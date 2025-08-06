import os
import yaml
from dotenv import load_dotenv
from crewai import Crew, Agent, Task
from crewai.memory import LongTermMemory
from crewai.tools import BaseTool

# Import des outils Make.com
from tools.make_tools import (
    MakeWebhookTool,
    FacebookPublisherTool,
    EmailSenderTool,
    CRMTool
)

# Import des outils Google Drive
from tools.google_drive_tools import (
    GoogleDriveImageSelector,
    GoogleDriveImageDownloader
)

# Charger les variables d'environnement
load_dotenv()

def load_crew_config():
    """Load crew configuration from YAML file"""
    with open("crew.yaml", "r", encoding="utf-8") as file:
        config = yaml.safe_load(file)
    return config

def create_tools_for_agent(agent_name: str, make_webhook_url: str):
    """Create appropriate tools for a given agent"""
    tools = []
    
    # Get Google Drive configuration
    credentials_file = os.getenv("GOOGLE_DRIVE_CREDENTIALS_FILE", "google-drive-credentials.json")
    folder_id = os.getenv("GOOGLE_DRIVE_FOLDER_ID", "")
    
    # Common tools
    make_webhook = MakeWebhookTool(make_webhook_url)
    
    # Google Drive tools
    if credentials_file and folder_id:
        google_drive_selector = GoogleDriveImageSelector(credentials_file, folder_id)
        google_drive_downloader = GoogleDriveImageDownloader(credentials_file)
        tools.extend([google_drive_selector, google_drive_downloader])
    
    # Specific tools per agent
    if "Publication Coordinator" in agent_name:
        tools.append(FacebookPublisherTool(make_webhook_url))
        tools.append(make_webhook)
    
    elif "Performance Analyst" in agent_name:
        tools.append(make_webhook)
    
    elif "Intelligent Planner" in agent_name:
        tools.append(make_webhook)
    
    elif "Budget Optimizer" in agent_name:
        tools.append(make_webhook)
    
    elif "Targeting Strategist" in agent_name:
        tools.append(CRMTool(make_webhook_url))
        tools.append(make_webhook)
    
    elif "Tunnel Agent" in agent_name:
        tools.append(make_webhook)
    
    elif "Technical Director" in agent_name:
        tools.append(make_webhook)
    
    return tools

def create_agents_from_config(config):
    """Create agents from YAML configuration"""
    agents = []
    agents_dict = {}  # Dictionary to map agents by name
    
    # Get Make.com webhook URL
    make_webhook_url = os.getenv("MAKE_WEBHOOK_URL", "http://localhost:8080/webhook")
    
    for agent_config in config['crew']['agents']:
        # Create tools for this agent
        tools = create_tools_for_agent(agent_config['name'], make_webhook_url)
        
        # Create agent with new syntax
        agent = Agent(
            name=agent_config['name'],
            role=agent_config['role'],
            goal=agent_config['goal'],
            backstory=f"I am {agent_config['name']}, {agent_config['role']}. My goal is to create content in French.",
            tools=tools,
            verbose=True,
            allow_delegation=True
        )
        agents.append(agent)
        agents_dict[agent_config['name']] = agent  # Store agent by name
    
    return agents, agents_dict

def create_tasks_from_config(config, agents_dict):
    """Create tasks from YAML configuration"""
    tasks = []
    
    # Create main task based on defined process
    if 'process' in config['crew'] and config['crew']['process']:
        process = config['crew']['process'][0]  # First process
        
        # Create task for each process step
        for step_name in process['steps']:
            # Find corresponding agent in dictionary
            agent = agents_dict.get(step_name)
            
            if agent:
                task = Task(
                    description=f"Execute step: {step_name}",
                    agent=agent,
                    expected_output=f"Result of {step_name} execution"
                )
                tasks.append(task)
    
    return tasks

def main():
    """Main function to execute the crew"""
    try:
        # Load configuration
        config = load_crew_config()
        
        # Create agents
        agents, agents_dict = create_agents_from_config(config)
        
        # Create tasks
        tasks = create_tasks_from_config(config, agents_dict)
        
        # Configure memory if specified
        long_term_memory = None
        if 'memory' in config['crew']:
            memory_config = config['crew']['memory']
            if memory_config['type'] == 'chromadb':
                # Use LongTermMemory with ChromaDB as backend
                long_term_memory = LongTermMemory(
                    path=memory_config['path']
                )
        
        # Create crew
        crew = Crew(
            agents=agents,
            tasks=tasks,
            long_term_memory=long_term_memory,
            verbose=True,
            process="sequential"  # or "hierarchical" based on your needs
        )
        
        # Define objective based on time of day
        from datetime import datetime
        current_hour = datetime.now().hour
        
        if 6 <= current_hour < 12:
            time_context = "morning"
            objective = "Crée du contenu inspirant et engageant pour le matin en français pour iFiveMe. Utilise le style moderne d'iFiveMe : questions engageantes comme 'Et si vous...?', langage positif comme 'Osez...', 'Découvrez...'. Focus sur les bénéfices de la carte d'affaires virtuelle, l'inspiration plutôt que les promos. Inclus des hashtags comme #iFiveMe #carteaffairesvirtuelle #réseautage #professionnelle #numérique #business #connexion #partage #entrepreneur #succès. SÉLECTIONNE une image existante de Google Drive (ne PAS créer de nouvelles images) et envoie à Make"
        elif 12 <= current_hour < 18:
            time_context = "afternoon"
            objective = "Crée du contenu inspirant et engageant pour l'après-midi en français pour iFiveMe. Utilise le style moderne d'iFiveMe : questions engageantes comme 'Et si vous...?', langage positif comme 'Osez l'efficacité', 'Découvrez la vraie modernité'. Focus sur le réseautage professionnel et les opportunités, l'inspiration plutôt que les promos. Inclus des hashtags comme #iFiveMe #productivité #business #réseautage #professionnelle #numérique #connexion #partage #entrepreneur #succès. SÉLECTIONNE une image existante de Google Drive (ne PAS créer de nouvelles images) et envoie à Make"
        else:
            time_context = "evening"
            objective = "Crée du contenu inspirant et engageant pour le soir en français pour iFiveMe. Utilise le style moderne d'iFiveMe : questions engageantes comme 'Et si vous...?', langage positif comme 'Osez...', 'Découvrez...'. Focus sur le développement professionnel et le réseautage stratégique, l'inspiration plutôt que les promos. Inclus des hashtags comme #iFiveMe #networking #business #réseautage #professionnelle #numérique #connexion #partage #entrepreneur #succès. SÉLECTIONNE une image existante de Google Drive (ne PAS créer de nouvelles images) et envoie à Make"
        
        print(f"🚀 Launching crew: {config['crew']['name']}")
        print(f"📋 Objective: {objective}")
        print(f"👥 Agents: {len(agents)}")
        print(f"📝 Tasks: {len(tasks)}")
        print(f"🔗 Make.com Webhook: {os.getenv('MAKE_WEBHOOK_URL', 'Not configured')}")
        print("=" * 50)
        
        # Execute crew
        result = crew.kickoff()
        
        print("\n" + "=" * 50)
        print("✅ FINAL RESULT")
        print("=" * 50)
        print(result)
        
        # Ajouter au tableau de bord
        try:
            from approval_dashboard import ApprovalDashboard
            approval_dashboard = ApprovalDashboard()
            publication_data = {
                'content': str(result),
                'image': 'downloaded_freepik__crer-une-image-dans-un-style-3d-semiraliste-inspir__48353.jpeg',
                'hashtags': ['#OffreSpéciale', '#NouveauProduit', '#Promotion', '#Exclusif', '#QualitéSupérieure']
            }
            approval_id = approval_dashboard.add_pending_publication(publication_data)
            print(f"\n📊 Publication ajoutée au dashboard d'approbation (ID: {approval_id[:8]})")
            print("💡 Pour approuver/rejeter: python3 approval_dashboard.py")
            print("🌐 Ou ouvrez: http://localhost:5001")
        except Exception as e:
            print(f"\n⚠️ Erreur dashboard d'approbation: {str(e)}")
        
    except Exception as e:
        print(f"❌ Error during execution: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Générateur automatique de publications
Maintient toujours au moins 10 publications en attente
"""

import json
import uuid
import time
import schedule
from datetime import datetime, timedelta
import random
import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from crewai.memory import LongTermMemory

# Load environment variables
load_dotenv()

class AutoPublicationGenerator:
    def __init__(self):
        self.pending_file = 'pending_approvals.json'
        self.min_pending = 10
        self.max_pending = 20
        
    def load_pending(self):
        """Charge les publications en attente"""
        try:
            with open(self.pending_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return []
    
    def save_pending(self, pending_list):
        """Sauvegarde les publications en attente"""
        with open(self.pending_file, 'w', encoding='utf-8') as f:
            json.dump(pending_list, f, ensure_ascii=False, indent=2)
    
    def count_pending(self):
        """Compte les publications en attente"""
        pending = self.load_pending()
        return len([p for p in pending if p.get('status') == 'pending'])
    
    def generate_publication(self):
        """Génère une nouvelle publication avec CrewAI"""
        print("🚀 Génération d'une nouvelle publication...")
        
        # Create agents with improved style
        content_creator = Agent(
            name="Content Creator",
            role="Creator of impactful editorial concepts",
            goal="Generate inspiring and engaging content ideas for iFiveMe that use modern, positive language. Focus on questions like 'Et si vous...?', 'Osez...', 'Découvrez...'. Create concepts that inspire rather than promote. All content must be in French with the iFiveMe style: engaging, modern, benefit-driven.",
            backstory="I am Content Creator, specialized in creating inspiring content concepts for iFiveMe.",
            verbose=False
        )
        
        copywriter = Agent(
            name="Copywriter",
            role="Modern, inspiring copywriter",
            goal="Write compelling French content in the iFiveMe style: inspiring, modern, and engaging. Use questions like 'Et si vous...?', positive language like 'Osez l'efficacité', 'Découvrez la vraie modernité'. Focus on benefits and inspiration, not promotions. Include relevant hashtags like #iFiveMe #carteaffairesvirtuelle #réseautage #professionnelle #numérique #business #connexion #partage #entrepreneur #succès.",
            backstory="I am Copywriter, specialized in writing modern, inspiring content for iFiveMe.",
            verbose=False
        )
        
        # Create tasks
        concept_task = Task(
            description="Create an inspiring content concept for iFiveMe virtual business card",
            agent=content_creator,
            expected_output="An inspiring content concept in the iFiveMe style"
        )
        
        writing_task = Task(
            description="Write a compelling Facebook post based on the concept",
            agent=copywriter,
            expected_output="A complete Facebook post in French with the iFiveMe style"
        )
        
        # Create crew
        crew = Crew(
            agents=[content_creator, copywriter],
            tasks=[concept_task, writing_task],
            verbose=False,
            process="sequential"
        )
        
        try:
            # Execute crew
            result = crew.kickoff()
            content = str(result)
            
            # Create publication
            publication = {
                "id": str(uuid.uuid4())[:8],
                "content": content,
                "image": "downloaded_freepik__crer-une-image-dans-un-style-3d-semiraliste-inspir__48353.jpeg",
                "status": "pending",
                "created_at": datetime.now().isoformat(),
                "agents": ["Content Creator", "Copywriter"],
                "style": "auto_generated"
            }
            
            # Add to pending
            pending = self.load_pending()
            pending.append(publication)
            self.save_pending(pending)
            
            print(f"✅ Publication générée avec succès - ID: {publication['id']}")
            return True
            
        except Exception as e:
            print(f"❌ Erreur lors de la génération: {str(e)}")
            return False
    
    def maintain_pending_count(self):
        """Maintient le nombre de publications en attente"""
        current_count = self.count_pending()
        print(f"📊 Publications en attente: {current_count}")
        
        if current_count < self.min_pending:
            needed = self.min_pending - current_count
            print(f"🔄 Génération de {needed} nouvelles publications...")
            
            for i in range(needed):
                success = self.generate_publication()
                if success:
                    print(f"✅ Publication {i+1}/{needed} générée")
                else:
                    print(f"❌ Échec de la génération {i+1}/{needed}")
                time.sleep(2)  # Pause entre les générations
        
        print(f"📊 Publications en attente après maintenance: {self.count_pending()}")
    
    def start_auto_generation(self):
        """Démarre la génération automatique"""
        print("🎯 GÉNÉRATEUR AUTOMATIQUE DE PUBLICATIONS")
        print("=" * 50)
        print(f"📊 Maintient {self.min_pending}-{self.max_pending} publications en attente")
        print("⏰ Vérification toutes les 30 minutes")
        print("🔄 Génération automatique en cours...")
        print("=" * 50)
        
        # Première génération immédiate
        self.maintain_pending_count()
        
        # Programmer les vérifications régulières
        schedule.every(30).minutes.do(self.maintain_pending_count)
        
        # Boucle principale
        while True:
            schedule.run_pending()
            time.sleep(60)  # Vérifier toutes les minutes

def main():
    """Fonction principale"""
    generator = AutoPublicationGenerator()
    
    try:
        generator.start_auto_generation()
    except KeyboardInterrupt:
        print("\n🛑 Générateur arrêté par l'utilisateur")
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")

if __name__ == "__main__":
    main() 
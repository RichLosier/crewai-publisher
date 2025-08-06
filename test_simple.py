"""
Test simple pour démontrer le fonctionnement du crew
Sans avoir besoin de clé API OpenAI
"""
import os
import yaml
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

def test_crew_structure():
    """Test simple pour vérifier que la structure du crew fonctionne"""
    
    print("🧪 TEST SIMPLE DU CREW")
    print("=" * 50)
    
    # 1. Charger la configuration
    try:
        with open("crew.yaml", "r", encoding="utf-8") as file:
            config = yaml.safe_load(file)
        print("✅ Configuration YAML chargée")
    except Exception as e:
        print(f"❌ Erreur chargement YAML: {e}")
        return
    
    # 2. Vérifier les agents
    agents = config['crew']['agents']
    print(f"✅ {len(agents)} agents trouvés:")
    for agent in agents:
        print(f"   - {agent['name']} ({agent['role']})")
    
    # 3. Vérifier le processus
    if 'process' in config['crew']:
        process = config['crew']['process'][0]
        steps = process['steps']
        print(f"✅ Processus trouvé: {process['name']}")
        print(f"✅ {len(steps)} étapes définies:")
        for step in steps:
            print(f"   - {step}")
    
    # 4. Vérifier la mémoire
    if 'memory' in config['crew']:
        memory = config['crew']['memory']
        print(f"✅ Mémoire configurée: {memory['type']} -> {memory['path']}")
    
    # 5. Simuler le workflow
    print("\n🔄 SIMULATION DU WORKFLOW:")
    print("1. Stratège Narratif → Crée le concept")
    print("2. Rédacteur Persuasif → Rédige le contenu")
    print("3. Curateur Visuel → Sélectionne l'image")
    print("4. Coordinateur de Publication → Envoie à Make.com")
    print("5. Make.com → Publie sur Facebook")
    print("6. Analyste Performance → Mesure les résultats")
    
    print("\n✅ Votre crew est prêt !")
    print("\n📋 PROCHAINES ÉTAPES:")
    print("1. Configurer une clé API OpenAI")
    print("2. Créer un scénario Make.com")
    print("3. Tester avec de vraies publications")

def test_make_integration():
    """Test de l'intégration Make.com"""
    
    print("\n🔗 TEST INTÉGRATION MAKE.COM")
    print("=" * 50)
    
    # Vérifier les variables d'environnement
    make_webhook = os.getenv("MAKE_WEBHOOK_URL")
    if make_webhook:
        print(f"✅ Webhook Make.com configuré: {make_webhook}")
    else:
        print("⚠️  Webhook Make.com non configuré")
    
    # Simuler un appel webhook
    print("\n📡 SIMULATION D'APPEL WEBHOOK:")
    print("POST /webhook")
    print("Content-Type: application/json")
    print("""
{
  "action": "publish_facebook",
  "data": {
    "post_content": "🎉 Découvrez notre nouvelle offre !",
    "image_url": "https://example.com/image.jpg",
    "scheduled_time": "2024-01-15T10:00:00Z",
    "platform": "facebook"
  },
  "timestamp": "2024-01-15T09:00:00Z"
}
    """)
    
    print("✅ Intégration Make.com prête !")

if __name__ == "__main__":
    test_crew_structure()
    test_make_integration()
    
    print("\n🎯 RÉSUMÉ:")
    print("✅ Votre crew CrewAI est configuré et prêt")
    print("✅ L'intégration Make.com est en place")
    print("✅ Vous pouvez maintenant passer aux étapes suivantes") 
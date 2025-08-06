#!/usr/bin/env python3
"""
Test complet de l'intégration CrewAI + Google Drive + Make.com
"""
import os
import requests
import json
from dotenv import load_dotenv
from tools.google_drive_tools import GoogleDriveImageSelector

# Charger les variables d'environnement
load_dotenv()

def test_complete_integration():
    """Test complet de l'intégration"""
    print("🔧 TEST COMPLET DE L'INTÉGRATION")
    print("=" * 50)
    
    # 1. Test Google Drive
    print("\n1️⃣ Test Google Drive...")
    try:
        credentials_file = os.getenv("GOOGLE_DRIVE_CREDENTIALS_FILE", "google-drive-credentials.json")
        folder_id = os.getenv("GOOGLE_DRIVE_FOLDER_ID", "")
        
        selector = GoogleDriveImageSelector(credentials_file, folder_id)
        result = selector._run("list")
        print(f"✅ Google Drive: {result[:100]}...")
    except Exception as e:
        print(f"❌ Google Drive: {str(e)}")
    
    # 2. Test Make.com
    print("\n2️⃣ Test Make.com...")
    try:
        webhook_url = os.getenv("MAKE_WEBHOOK_URL", "")
        
        test_data = {
            "action": "publish_facebook",
            "data": {
                "post_content": "Test de publication depuis CrewAI",
                "image_url": "test_image.jpg",
                "platform": "facebook"
            }
        }
        
        response = requests.post(
            webhook_url,
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"📊 Make.com - Statut: {response.status_code}")
        print(f"📋 Make.com - Réponse: {response.text}")
        
        if response.status_code == 200:
            print("✅ Make.com: Connexion réussie")
        else:
            print(f"⚠️ Make.com: Problème de connexion (statut {response.status_code})")
            
    except Exception as e:
        print(f"❌ Make.com: {str(e)}")
    
    # 3. Test CrewAI
    print("\n3️⃣ Test CrewAI...")
    try:
        from main import main
        print("✅ CrewAI: Import réussi")
    except Exception as e:
        print(f"❌ CrewAI: {str(e)}")
    
    # 4. Recommandations
    print("\n4️⃣ Recommandations...")
    print("📋 Si Make.com ne fonctionne pas:")
    print("   - Allez dans Make.com et activez votre scénario")
    print("   - Vérifiez que le webhook est bien configuré")
    print("   - Testez avec le simulateur local si nécessaire")
    
    print("\n📋 Si Google Drive ne fonctionne pas:")
    print("   - Vérifiez que le dossier est partagé avec le Service Account")
    print("   - Vérifiez que les credentials sont corrects")
    
    print("\n📋 Si CrewAI ne fonctionne pas:")
    print("   - Vérifiez que OpenAI API key est valide")
    print("   - Vérifiez que toutes les dépendances sont installées")

if __name__ == "__main__":
    test_complete_integration() 
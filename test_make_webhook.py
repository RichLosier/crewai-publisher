#!/usr/bin/env python3
"""
Test simple pour vérifier la connexion à Make.com
"""
import os
import requests
import json
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

def test_make_webhook():
    """Test simple de la connexion à Make.com"""
    try:
        # Récupérer l'URL du webhook
        webhook_url = os.getenv("MAKE_WEBHOOK_URL", "")
        
        print(f"🔧 Configuration:")
        print(f"   Webhook URL: {webhook_url}")
        
        if not webhook_url:
            print("❌ URL du webhook non configurée")
            return
        
        # Données de test
        test_data = {
            "action": "test_connection",
            "data": {
                "message": "Test de connexion depuis CrewAI",
                "timestamp": "2024-08-03T10:45:00Z"
            }
        }
        
        print(f"🔍 Test de connexion à Make.com...")
        
        # Envoyer la requête
        response = requests.post(
            webhook_url,
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"📊 Statut de la réponse: {response.status_code}")
        print(f"📋 Contenu de la réponse: {response.text}")
        
        if response.status_code == 200:
            print("✅ Connexion à Make.com réussie !")
        else:
            print(f"❌ Erreur de connexion: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_make_webhook() 
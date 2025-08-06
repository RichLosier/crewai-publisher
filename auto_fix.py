#!/usr/bin/env python3
"""
Script de récupération automatique pour CrewAI
"""
import os
import subprocess
import sys
from dotenv import load_dotenv

load_dotenv()

def auto_fix():
    """Corrige automatiquement les problèmes courants"""
    print("🔧 RÉCUPÉRATION AUTOMATIQUE")
    print("=" * 40)
    
    # 1. Vérifier et corriger les dépendances
    print("\n1️⃣ Vérification des dépendances...")
    try:
        import crewai
        print("   ✅ crewai installé")
    except:
        print("   🔧 Installation de crewai...")
        subprocess.run([sys.executable, "-m", "pip", "install", "crewai"])
    
    try:
        import yaml
        print("   ✅ pyyaml installé")
    except:
        print("   🔧 Installation de pyyaml...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyyaml"])
    
    try:
        import requests
        print("   ✅ requests installé")
    except:
        print("   🔧 Installation de requests...")
        subprocess.run([sys.executable, "-m", "pip", "install", "requests"])
    
    try:
        from google.oauth2 import service_account
        print("   ✅ google-auth installé")
    except:
        print("   🔧 Installation de google-auth...")
        subprocess.run([sys.executable, "-m", "pip", "install", "google-auth", "google-api-python-client"])
    
    # 2. Vérifier et corriger le fichier .env
    print("\n2️⃣ Vérification du fichier .env...")
    env_file = ".env"
    if not os.path.exists(env_file):
        print("   🔧 Création du fichier .env...")
        with open(env_file, "w") as f:
            f.write("# Configuration CrewAI\n")
            f.write("OPENAI_API_KEY=your_openai_api_key_here\n")
            f.write("MAKE_WEBHOOK_URL=https://hook.us2.make.com/cojopjk9yp1vc18zxxlryodv29qfvgqb\n")
            f.write("GOOGLE_DRIVE_CREDENTIALS_FILE=google-drive-credentials.json\n")
            f.write("GOOGLE_DRIVE_FOLDER_ID=17-oCs14_qoUrEdHGk7nflOU86SdABeO1\n")
        print("   ✅ Fichier .env créé")
    else:
        print("   ✅ Fichier .env existe")
    
    # 3. Vérifier et corriger les outils
    print("\n3️⃣ Vérification des outils...")
    tools_dir = "tools"
    if not os.path.exists(tools_dir):
        print("   🔧 Création du dossier tools...")
        os.makedirs(tools_dir)
    
    # 4. Test de connexion Google Drive
    print("\n4️⃣ Test Google Drive...")
    try:
        from tools.google_drive_tools import GoogleDriveImageSelector
        credentials_file = os.getenv("GOOGLE_DRIVE_CREDENTIALS_FILE", "google-drive-credentials.json")
        folder_id = os.getenv("GOOGLE_DRIVE_FOLDER_ID", "")
        
        if os.path.exists(credentials_file) and folder_id:
            selector = GoogleDriveImageSelector(credentials_file, folder_id)
            result = selector._run("list")
            print("   ✅ Google Drive fonctionne")
        else:
            print("   ⚠️ Google Drive: Vérifiez credentials et folder_id")
    except Exception as e:
        print(f"   ❌ Google Drive: {str(e)}")
    
    # 5. Test de connexion Make.com
    print("\n5️⃣ Test Make.com...")
    try:
        import requests
        webhook_url = os.getenv("MAKE_WEBHOOK_URL", "")
        if webhook_url:
            response = requests.post(
                webhook_url,
                json={"test": "connection"},
                timeout=5
            )
            if response.status_code == 200:
                print("   ✅ Make.com fonctionne")
            else:
                print(f"   ⚠️ Make.com: Statut {response.status_code}")
        else:
            print("   ⚠️ Make.com: URL non configurée")
    except Exception as e:
        print(f"   ❌ Make.com: {str(e)}")
    
    # 6. Recommandations finales
    print("\n6️⃣ Recommandations:")
    print("   📋 Si Google Drive ne fonctionne pas:")
    print("      - Vérifiez que le dossier est partagé avec le Service Account")
    print("      - Vérifiez que les credentials sont corrects")
    print("   📋 Si Make.com ne fonctionne pas:")
    print("      - Activez votre scénario dans Make.com")
    print("      - Vérifiez que le webhook est configuré")
    print("   📋 Pour tester:")
    print("      - python3 main.py")
    print("      - ou python3 main_test_mode.py (mode local)")

if __name__ == "__main__":
    auto_fix() 
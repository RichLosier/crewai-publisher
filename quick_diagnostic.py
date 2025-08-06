#!/usr/bin/env python3
"""
Diagnostic rapide pour identifier le problème
"""
import os
import sys
from dotenv import load_dotenv

load_dotenv()

def quick_diagnostic():
    """Diagnostic rapide du système"""
    print("🔧 DIAGNOSTIC RAPIDE")
    print("=" * 40)
    
    # 1. Vérifier les fichiers essentiels
    print("\n1️⃣ Fichiers essentiels:")
    files_to_check = [
        "main.py",
        "crew.yaml", 
        ".env",
        "google-drive-credentials.json",
        "tools/google_drive_tools.py",
        "tools/make_tools.py"
    ]
    
    for file in files_to_check:
        if os.path.exists(file):
            print(f"   ✅ {file}")
        else:
            print(f"   ❌ {file} - MANQUANT")
    
    # 2. Vérifier les variables d'environnement
    print("\n2️⃣ Variables d'environnement:")
    env_vars = [
        "OPENAI_API_KEY",
        "MAKE_WEBHOOK_URL", 
        "GOOGLE_DRIVE_CREDENTIALS_FILE",
        "GOOGLE_DRIVE_FOLDER_ID"
    ]
    
    for var in env_vars:
        value = os.getenv(var, "")
        if value:
            print(f"   ✅ {var}: {'*' * 10}")  # Masquer les valeurs sensibles
        else:
            print(f"   ❌ {var}: MANQUANT")
    
    # 3. Test des imports
    print("\n3️⃣ Test des imports:")
    try:
        import crewai
        print("   ✅ crewai")
    except:
        print("   ❌ crewai - INSTALLER: pip install crewai")
    
    try:
        import yaml
        print("   ✅ pyyaml")
    except:
        print("   ❌ pyyaml - INSTALLER: pip install pyyaml")
    
    try:
        import requests
        print("   ✅ requests")
    except:
        print("   ❌ requests - INSTALLER: pip install requests")
    
    try:
        from google.oauth2 import service_account
        print("   ✅ google-auth")
    except:
        print("   ❌ google-auth - INSTALLER: pip install google-auth google-api-python-client")
    
    # 4. Recommandations
    print("\n4️⃣ Actions recommandées:")
    print("   📋 Si des fichiers manquent:")
    print("      - Relancez la configuration")
    print("   📋 Si des variables manquent:")
    print("      - Vérifiez le fichier .env")
    print("   📋 Si des imports échouent:")
    print("      - Installez les dépendances manquantes")
    print("   📋 Si tout est OK:")
    print("      - Lancez: python3 main.py")

if __name__ == "__main__":
    quick_diagnostic() 
#!/usr/bin/env python3
"""
Test simple pour vérifier l'accès à Google Drive
"""
import os
from dotenv import load_dotenv
from tools.google_drive_tools import GoogleDriveImageSelector

# Charger les variables d'environnement
load_dotenv()

def test_google_drive():
    """Test simple de l'accès à Google Drive"""
    try:
        # Récupérer la configuration
        credentials_file = os.getenv("GOOGLE_DRIVE_CREDENTIALS_FILE", "google-drive-credentials.json")
        folder_id = os.getenv("GOOGLE_DRIVE_FOLDER_ID", "")
        
        print(f"🔧 Configuration:")
        print(f"   Credentials file: {credentials_file}")
        print(f"   Folder ID: {folder_id}")
        
        # Vérifier que les fichiers existent
        if not os.path.exists(credentials_file):
            print(f"❌ Fichier credentials non trouvé: {credentials_file}")
            return
        
        print(f"✅ Fichier credentials trouvé")
        
        # Créer l'outil
        selector = GoogleDriveImageSelector(credentials_file, folder_id)
        
        print(f"🔍 Test de liste des images...")
        result = selector._run("list")
        print(f"📋 Résultat: {result}")
        
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_google_drive() 
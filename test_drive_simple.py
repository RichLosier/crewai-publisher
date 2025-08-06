#!/usr/bin/env python3
"""
Test simple pour vérifier l'accès à Google Drive
"""
import os
from dotenv import load_dotenv
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# Charger les variables d'environnement
load_dotenv()

def test_drive_access():
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
        
        # Créer le service
        creds = Credentials.from_service_account_file(
            credentials_file,
            scopes=['https://www.googleapis.com/auth/drive.readonly']
        )
        service = build('drive', 'v3', credentials=creds)
        
        print(f"🔍 Test de connexion à Google Drive...")
        
        # Test simple : lister les fichiers de l'utilisateur
        results = service.files().list(
            pageSize=5,
            fields="files(id,name)"
        ).execute()
        
        files = results.get('files', [])
        print(f"✅ Connexion réussie ! Fichiers trouvés: {len(files)}")
        
        if files:
            print("📋 Premiers fichiers:")
            for file in files:
                print(f"   - {file['name']} (ID: {file['id']})")
        
        # Test spécifique du dossier
        print(f"\n🔍 Test du dossier spécifique (ID: {folder_id})...")
        try:
            folder = service.files().get(fileId=folder_id).execute()
            print(f"✅ Dossier trouvé: {folder['name']}")
            
            # Lister les fichiers dans ce dossier
            results = service.files().list(
                q=f"'{folder_id}' in parents",
                fields="files(id,name,mimeType)",
                pageSize=10
            ).execute()
            
            files = results.get('files', [])
            print(f"📋 Fichiers dans le dossier: {len(files)}")
            
            for file in files:
                print(f"   - {file['name']} ({file['mimeType']})")
                
        except Exception as e:
            print(f"❌ Erreur avec le dossier: {str(e)}")
        
    except Exception as e:
        print(f"❌ Erreur générale: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_drive_access() 
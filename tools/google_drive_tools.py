"""
Outils CrewAI pour l'intégration avec Google Drive
"""
import os
import json
from typing import List, Dict, Any
from crewai.tools import BaseTool
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import io

class GoogleDriveImageSelector(BaseTool):
    """Outil pour lister et sélectionner des images depuis Google Drive"""

    name: str = "google_drive_image_selector"
    description: str = "Liste et sélectionne des images depuis Google Drive pour les publications"

    def __init__(self, credentials_file: str, folder_id: str):
        super().__init__()
        self._credentials_file = credentials_file
        self._folder_id = folder_id
        self._service = None

    def _get_service(self):
        """Initialise le service Google Drive"""
        if self._service is None:
            creds = Credentials.from_service_account_file(
                self._credentials_file,
                scopes=['https://www.googleapis.com/auth/drive.readonly']
            )
            self._service = build('drive', 'v3', credentials=creds)
        return self._service

    def _run(self, action: str = "list", context: str = None) -> str:
        """
        Liste ou sélectionne des images depuis Google Drive

        Args:
            action: "list" pour lister toutes les images, "select" pour sélectionner selon le contexte
            context: Contexte pour la sélection (ex: "coaching", "productivité")
        """
        try:
            service = self._get_service()
            
            # Lister les fichiers dans le dossier
            results = service.files().list(
                q=f"'{self._folder_id}' in parents and (mimeType contains 'image/')",
                fields="files(id,name,mimeType,webContentLink)",
                orderBy="name"
            ).execute()
            
            files = results.get('files', [])
            
            if not files:
                return "❌ Aucune image trouvée dans le dossier Google Drive"
            
            if action == "list":
                # Lister toutes les images
                image_list = []
                for file in files:
                    image_list.append(f"📸 {file['name']} (ID: {file['id']})")
                
                return f"✅ Images disponibles dans Google Drive:\n" + "\n".join(image_list)
            
            elif action == "select":
                # Sélectionner une image selon le contexte
                if context:
                    # Logique simple de sélection basée sur le nom
                    context_keywords = context.lower().split()
                    selected_images = []
                    
                    for file in files:
                        file_name = file['name'].lower()
                        for keyword in context_keywords:
                            if keyword in file_name:
                                selected_images.append(file)
                                break
                    
                    if selected_images:
                        # Retourner la première image trouvée
                        selected = selected_images[0]
                        return f"✅ Image sélectionnée: {selected['name']} (ID: {selected['id']})"
                    else:
                        # Retourner la première image si aucune correspondance
                        selected = files[0]
                        return f"✅ Image par défaut sélectionnée: {selected['name']} (ID: {selected['id']})"
                else:
                    # Retourner la première image
                    selected = files[0]
                    return f"✅ Image sélectionnée: {selected['name']} (ID: {selected['id']})"
            
            return "❌ Action non reconnue. Utilisez 'list' ou 'select'"
            
        except Exception as e:
            return f"❌ Erreur lors de l'accès à Google Drive: {str(e)}"

class GoogleDriveImageDownloader(BaseTool):
    """Outil pour télécharger des images depuis Google Drive"""

    name: str = "google_drive_image_downloader"
    description: str = "Télécharge une image depuis Google Drive par son ID"

    def __init__(self, credentials_file: str):
        super().__init__()
        self._credentials_file = credentials_file
        self._service = None

    def _get_service(self):
        """Initialise le service Google Drive"""
        if self._service is None:
            creds = Credentials.from_service_account_file(
                self._credentials_file,
                scopes=['https://www.googleapis.com/auth/drive.readonly']
            )
            self._service = build('drive', 'v3', credentials=creds)
        return self._service

    def _run(self, file_id: str) -> str:
        """
        Télécharge une image depuis Google Drive

        Args:
            file_id: ID du fichier à télécharger
        """
        try:
            service = self._get_service()
            
            # Obtenir les informations du fichier
            file = service.files().get(fileId=file_id).execute()
            
            # Télécharger le fichier
            request = service.files().get_media(fileId=file_id)
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)
            
            done = False
            while done is False:
                status, done = downloader.next_chunk()
            
            # Sauvegarder le fichier
            filename = f"downloaded_{file['name']}"
            with open(filename, 'wb') as f:
                f.write(fh.getvalue())
            
            return f"✅ Image téléchargée: {filename}"
            
        except Exception as e:
            return f"❌ Erreur lors du téléchargement: {str(e)}" 
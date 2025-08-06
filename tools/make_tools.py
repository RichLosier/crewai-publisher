"""
Outils CrewAI pour l'intégration avec Make.com
"""
import requests
import json
from typing import Dict, Any
from crewai.tools import BaseTool
from datetime import datetime

class MakeWebhookTool(BaseTool):
    """Outil pour déclencher des webhooks Make.com"""
    
    name: str = "make_webhook"
    description: str = "Déclenche un webhook Make.com pour exécuter des actions automatisées"
    
    def __init__(self, webhook_url: str):
        super().__init__()
        self._webhook_url = webhook_url
    
    def _run(self, action: str, data: Dict[str, Any]) -> str:
        """
        Déclenche un webhook Make.com
        
        Args:
            action: Type d'action à exécuter (publish_facebook, send_email, etc.)
            data: Données à envoyer au webhook
        """
        try:
            payload = {
                "action": action,
                "data": data,
                "timestamp": str(datetime.now())
            }
            
            response = requests.post(
                self._webhook_url,
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                return f"✅ Action '{action}' exécutée avec succès via Make.com"
            else:
                return f"❌ Erreur lors de l'exécution de l'action '{action}': {response.text}"
                
        except Exception as e:
            return f"❌ Erreur de connexion à Make.com: {str(e)}"

class FacebookPublisherTool(BaseTool):
    """Outil spécialisé pour la publication Facebook via Make.com"""
    
    name: str = "facebook_publisher"
    description: str = "Publie du contenu sur Facebook via Make.com"
    
    def __init__(self, make_webhook_url: str):
        super().__init__()
        self._make_webhook = MakeWebhookTool(make_webhook_url)
    
    def _run(self, post_content: str, image_url: str = None, scheduled_time: str = None) -> str:
        """
        Publie du contenu sur Facebook
        
        Args:
            post_content: Contenu du post Facebook
            image_url: URL de l'image (optionnel)
            scheduled_time: Heure de publication programmée (optionnel)
        """
        data = {
            "post_content": post_content,
            "image_url": image_url,
            "scheduled_time": scheduled_time,
            "platform": "facebook"
        }
        
        return self._make_webhook._run("publish_facebook", data)

class EmailSenderTool(BaseTool):
    """Outil pour l'envoi d'emails via Make.com"""
    
    name: str = "email_sender"
    description: str = "Envoie des emails via Make.com"
    
    def __init__(self, make_webhook_url: str):
        super().__init__()
        self._make_webhook = MakeWebhookTool(make_webhook_url)
    
    def _run(self, to_email: str, subject: str, body: str) -> str:
        """
        Envoie un email
        
        Args:
            to_email: Adresse email du destinataire
            subject: Sujet de l'email
            body: Corps de l'email
        """
        data = {
            "to_email": to_email,
            "subject": subject,
            "body": body
        }
        
        return self._make_webhook._run("send_email", data)

class CRMTool(BaseTool):
    """Outil pour interagir avec le CRM via Make.com"""
    
    name: str = "crm_tool"
    description: str = "Interagit avec le CRM via Make.com"
    
    def __init__(self, make_webhook_url: str):
        super().__init__()
        self._make_webhook = MakeWebhookTool(make_webhook_url)
    
    def _run(self, action: str, customer_data: Dict[str, Any]) -> str:
        """
        Effectue des actions CRM
        
        Args:
            action: Type d'action (create_lead, update_customer, etc.)
            customer_data: Données du client
        """
        data = {
            "action": action,
            "customer_data": customer_data
        }
        
        return self._make_webhook._run("crm_action", data) 
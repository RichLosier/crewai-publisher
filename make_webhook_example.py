"""
Exemple de webhook Make.com pour tester l'intégration
Ce fichier simule ce que Make.com devrait recevoir et traiter
"""
from flask import Flask, request, jsonify
import json
import logging

app = Flask(__name__)

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/webhook', methods=['POST'])
def webhook_handler():
    """Gestionnaire de webhook pour Make.com"""
    try:
        data = request.get_json()
        logger.info(f"📥 Webhook reçu: {json.dumps(data, indent=2)}")
        
        action = data.get('action')
        payload_data = data.get('data', {})
        
        # Traitement selon le type d'action
        if action == 'publish_facebook':
            result = handle_facebook_publish(payload_data)
        elif action == 'send_email':
            result = handle_email_send(payload_data)
        elif action == 'crm_action':
            result = handle_crm_action(payload_data)
        else:
            result = f"❌ Action non reconnue: {action}"
        
        logger.info(f"✅ Résultat: {result}")
        return jsonify({"status": "success", "result": result})
        
    except Exception as e:
        logger.error(f"❌ Erreur dans le webhook: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

def handle_facebook_publish(data):
    """Gère la publication Facebook"""
    post_content = data.get('post_content', '')
    image_url = data.get('image_url')
    scheduled_time = data.get('scheduled_time')
    platform = data.get('platform', 'facebook')
    
    logger.info(f"📘 Publication {platform}:")
    logger.info(f"   Contenu: {post_content[:100]}...")
    logger.info(f"   Image: {image_url}")
    logger.info(f"   Programmé: {scheduled_time}")
    
    # Simulation de la publication
    return f"✅ Post publié sur {platform} avec succès"

def handle_email_send(data):
    """Gère l'envoi d'email"""
    to_email = data.get('to_email')
    subject = data.get('subject')
    body = data.get('body')
    
    logger.info(f"📧 Email envoyé:")
    logger.info(f"   À: {to_email}")
    logger.info(f"   Sujet: {subject}")
    logger.info(f"   Corps: {body[:100]}...")
    
    # Simulation de l'envoi
    return f"✅ Email envoyé à {to_email}"

def handle_crm_action(data):
    """Gère les actions CRM"""
    action = data.get('action')
    customer_data = data.get('customer_data', {})
    
    logger.info(f"👤 Action CRM '{action}':")
    logger.info(f"   Données client: {customer_data}")
    
    # Simulation de l'action CRM
    return f"✅ Action CRM '{action}' exécutée"

@app.route('/health', methods=['GET'])
def health_check():
    """Point de terminaison pour vérifier la santé du service"""
    return jsonify({"status": "healthy", "service": "make-webhook-simulator"})

if __name__ == '__main__':
    logger.info("🚀 Démarrage du simulateur de webhook Make.com...")
    logger.info("📡 Webhook disponible sur: http://localhost:8080/webhook")
    logger.info("🏥 Health check sur: http://localhost:8080/health")
    
    app.run(host='0.0.0.0', port=8080, debug=True) 
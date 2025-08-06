#!/usr/bin/env python3
"""
Dashboard d'approbation pour les publications CrewAI
Interface web pour approuver/rejeter les publications avant publication sur Facebook
"""

import os
import json
import uuid
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for
from dotenv import load_dotenv
import requests

# Charger les variables d'environnement
load_dotenv()

app = Flask(__name__, static_folder='static')
app.secret_key = 'crewai-approval-secret-key'

# Fichier de stockage des publications
PUBLICATIONS_FILE = 'publications.json'
PENDING_FILE = 'pending_approvals.json'

class ApprovalDashboard:
    def __init__(self):
        self.publications_file = PUBLICATIONS_FILE
        self.pending_file = PENDING_FILE
        self.make_webhook_url = os.getenv('MAKE_WEBHOOK_URL', 'http://localhost:8080/webhook')
    
    def load_publications(self):
        """Charge toutes les publications"""
        try:
            with open(self.publications_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return []
    
    def load_pending(self):
        """Charge les publications en attente d'approbation"""
        try:
            with open(self.pending_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return []
    
    def save_pending(self, pending_list):
        """Sauvegarde les publications en attente"""
        with open(self.pending_file, 'w', encoding='utf-8') as f:
            json.dump(pending_list, f, indent=2, ensure_ascii=False)
    
    def add_pending_publication(self, publication_data):
        """Ajoute une publication en attente d'approbation"""
        pending = self.load_pending()
        
        # Créer une nouvelle publication en attente
        pending_publication = {
            'id': str(uuid.uuid4()),
            'timestamp': datetime.now().isoformat(),
            'status': 'pending',
            'publication': publication_data,
            'approved_by': None,
            'approved_at': None,
            'rejected_reason': None
        }
        
        pending.append(pending_publication)
        self.save_pending(pending)
        return pending_publication['id']
    
    def approve_publication(self, publication_id):
        """Approuve une publication et l'envoie à Make.com"""
        pending = self.load_pending()
        publications = self.load_publications()
        
        # Trouver la publication en attente
        for pub in pending:
            if pub['id'] == publication_id:
                # Mettre à jour le statut
                pub['status'] = 'approved'
                pub['approved_at'] = datetime.now().isoformat()
                pub['approved_by'] = 'Admin'
                
                # Ajouter aux publications approuvées
                approved_pub = {
                    'id': pub['id'],
                    'timestamp': pub['timestamp'],
                    'status': 'approved',
                    'content': pub['publication'].get('content', ''),
                    'image': pub['publication'].get('image', ''),
                    'approved_at': pub['approved_at'],
                    'approved_by': pub['approved_by']
                }
                publications.append(approved_pub)
                
                # Sauvegarder
                with open(self.publications_file, 'w', encoding='utf-8') as f:
                    json.dump(publications, f, indent=2, ensure_ascii=False)
                
                # Envoyer à Make.com
                self.send_to_make(pub['publication'])
                
                # Retirer des en attente
                pending = [p for p in pending if p['id'] != publication_id]
                self.save_pending(pending)
                
                return True
        
        return False
    
    def reject_publication(self, publication_id):
        """Rejette une publication"""
        pending = self.load_pending()
        
        for pub in pending:
            if pub['id'] == publication_id:
                pub['status'] = 'rejected'
                pub['rejected_at'] = datetime.now().isoformat()
                pub['rejected_by'] = 'Admin'
                
                self.save_pending(pending)
                return True
        
        return False
    
    def send_to_make(self, publication_data):
        """Envoie la publication approuvée à Make.com"""
        try:
            payload = {
                "action": "publish_facebook",
                "data": {
                    "content": publication_data.get('content', ''),
                    "image": publication_data.get('image', ''),
                    "hashtags": publication_data.get('hashtags', []),
                    "timestamp": datetime.now().isoformat()
                }
            }
            
            response = requests.post(
                self.make_webhook_url,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code == 200:
                print(f"✅ Publication envoyée à Make.com avec succès")
                return True
            else:
                print(f"❌ Erreur lors de l'envoi à Make.com: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Erreur de connexion à Make.com: {str(e)}")
            return False

# Instance globale du dashboard
dashboard = ApprovalDashboard()

@app.route('/')
def index():
    """Page principale du dashboard"""
    pending = dashboard.load_pending()
    publications = dashboard.load_publications()
    
    return render_template('approval_dashboard.html', 
                         pending=pending, 
                         publications=publications)

@app.route('/approve/<publication_id>')
def approve_publication(publication_id):
    """Approuve une publication"""
    if dashboard.approve_publication(publication_id):
        return jsonify({"success": True, "message": "Publication approuvée et envoyée à Make.com"})
    else:
        return jsonify({"success": False, "message": "Publication non trouvée"})

@app.route('/reject/<publication_id>', methods=['GET'])
def reject_publication(publication_id):
    """Rejette une publication"""
    if dashboard.reject_publication(publication_id):
        return jsonify({"success": True, "message": "Publication rejetée"})
    else:
        return jsonify({"success": False, "message": "Publication non trouvée"})

@app.route('/api/pending')
def api_pending():
    """API pour récupérer les publications en attente"""
    pending = dashboard.load_pending()
    return jsonify(pending)

@app.route('/api/publications')
def api_publications():
    """API pour récupérer toutes les publications"""
    publications = dashboard.load_publications()
    return jsonify(publications)

if __name__ == '__main__':
    print("🎯 DASHBOARD D'APPROBATION CREWAI")
    print("=" * 50)
    print("🌐 Interface web: http://localhost:5001")
    print("📊 Visualisez et approuvez vos publications")
    print("🔗 Make.com sera notifié automatiquement")
    print("=" * 50)
    
    # Get port from environment variable (for deployment)
    port = int(os.environ.get('PORT', 5001))
    app.run(debug=False, host='0.0.0.0', port=port) 
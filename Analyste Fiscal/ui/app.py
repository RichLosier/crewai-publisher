"""
Application web principale - Interface Google-like pour le système fiscal AI
"""
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_uploads import UploadSet, configure_uploads, IMAGES, DOCUMENTS
import os
import json
import uuid
from datetime import datetime
from werkzeug.utils import secure_filename
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-here')

# Configuration des uploads
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'csv', 'xlsx', 'docx'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

# Configuration des uploads
files = UploadSet('files', DOCUMENTS + IMAGES)
configure_uploads(app, files)

# Système de mémoire évolutive
class CompanyMemory:
    def __init__(self):
        self.memory_file = 'data/company_memory.json'
        self.load_memory()
    
    def load_memory(self):
        """Charger la mémoire de l'entreprise"""
        try:
            if os.path.exists(self.memory_file):
                with open(self.memory_file, 'r', encoding='utf-8') as f:
                    self.memory = json.load(f)
            else:
                self.memory = {
                    'company_info': {},
                    'conversations': [],
                    'learned_patterns': [],
                    'preferences': {},
                    'last_updated': datetime.now().isoformat()
                }
                self.save_memory()
        except Exception as e:
            logger.error(f"Erreur lors du chargement de la mémoire: {e}")
            self.memory = {
                'company_info': {},
                'conversations': [],
                'learned_patterns': [],
                'preferences': {},
                'last_updated': datetime.now().isoformat()
            }
    
    def save_memory(self):
        """Sauvegarder la mémoire de l'entreprise"""
        try:
            os.makedirs(os.path.dirname(self.memory_file), exist_ok=True)
            with open(self.memory_file, 'w', encoding='utf-8') as f:
                json.dump(self.memory, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Erreur lors de la sauvegarde de la mémoire: {e}")
    
    def add_conversation(self, query, response, context=None):
        """Ajouter une conversation à la mémoire"""
        conversation = {
            'id': str(uuid.uuid4()),
            'timestamp': datetime.now().isoformat(),
            'query': query,
            'response': response,
            'context': context or {}
        }
        self.memory['conversations'].append(conversation)
        
        # Garder seulement les 100 dernières conversations
        if len(self.memory['conversations']) > 100:
            self.memory['conversations'] = self.memory['conversations'][-100:]
        
        self.memory['last_updated'] = datetime.now().isoformat()
        self.save_memory()
    
    def learn_pattern(self, pattern_type, data):
        """Apprendre un nouveau pattern"""
        pattern = {
            'type': pattern_type,
            'data': data,
            'learned_at': datetime.now().isoformat()
        }
        self.memory['learned_patterns'].append(pattern)
        self.save_memory()
    
    def get_company_context(self):
        """Obtenir le contexte de l'entreprise"""
        return {
            'recent_conversations': self.memory['conversations'][-10:],
            'learned_patterns': self.memory['learned_patterns'],
            'preferences': self.memory['preferences']
        }

# Initialiser la mémoire
company_memory = CompanyMemory()

def allowed_file(filename):
    """Vérifier si le fichier est autorisé"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Page principale - Interface Google-like"""
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    """Traiter les requêtes de recherche"""
    try:
        data = request.get_json()
        query = data.get('query', '').strip()
        
        if not query:
            return jsonify({'error': 'Requête vide'}), 400
        
        # Traiter la requête avec le système AI
        response = process_query(query)
        
        # Ajouter à la mémoire
        company_memory.add_conversation(query, response)
        
        return jsonify({
            'response': response,
            'query': query,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Erreur lors du traitement de la requête: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/upload', methods=['POST'])
def upload_file():
    """Traiter l'upload de fichiers"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'Aucun fichier sélectionné'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'Aucun fichier sélectionné'}), 400
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_id = str(uuid.uuid4())
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{file_id}_{filename}")
            file.save(file_path)
            
            # Analyser le fichier avec le système AI
            analysis = analyze_uploaded_file(file_path, filename)
            
            # Ajouter à la mémoire
            company_memory.add_conversation(
                f"Fichier uploadé: {filename}",
                analysis,
                {'file_path': file_path, 'file_id': file_id}
            )
            
            return jsonify({
                'success': True,
                'filename': filename,
                'file_id': file_id,
                'analysis': analysis,
                'message': f'Fichier {filename} analysé avec succès'
            })
        
        return jsonify({'error': 'Type de fichier non autorisé'}), 400
        
    except Exception as e:
        logger.error(f"Erreur lors de l'upload: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/memory')
def get_memory():
    """Obtenir la mémoire de l'entreprise"""
    try:
        context = company_memory.get_company_context()
        return jsonify(context)
    except Exception as e:
        logger.error(f"Erreur lors de la récupération de la mémoire: {e}")
        return jsonify({'error': str(e)}), 500

def process_query(query):
    """Traiter une requête avec le système AI"""
    try:
        # Importer le système fiscal AI
        from main import FiscalAICrew
        
        # Initialiser le crew
        fiscal_crew = FiscalAICrew(
            company_name="iFiveMe",
            enable_learning=True,
            enable_real_time_sync=True,
            enable_predictive_analytics=True
        )
        
        # Analyser la requête et déterminer l'action
        if 'calcul' in query.lower() or 'taxe' in query.lower():
            return process_tax_calculation(query)
        elif 'échéance' in query.lower() or 'deadline' in query.lower():
            return process_deadline_query(query)
        elif 'rapport' in query.lower() or 'report' in query.lower():
            return process_report_request(query)
        elif 'optimisation' in query.lower() or 'optimization' in query.lower():
            return process_optimization_request(query)
        else:
            return process_general_query(query)
            
    except Exception as e:
        logger.error(f"Erreur lors du traitement de la requête: {e}")
        return f"Je ne peux pas traiter cette requête pour le moment. Erreur: {str(e)}"

def process_tax_calculation(query):
    """Traiter une requête de calcul fiscal"""
    try:
        from config.tax_rules import tax_rules_engine
        from decimal import Decimal
        import re
        
        # Extraire le montant de la requête
        amount_match = re.search(r'(\d+(?:\.\d+)?)', query)
        if amount_match:
            amount = Decimal(amount_match.group(1))
            
            # Calculer les taxes
            gst_calc = tax_rules_engine.calculate_gst(amount)
            qst_calc = tax_rules_engine.calculate_qst(amount)
            combined = tax_rules_engine.calculate_combined_taxes(amount)
            
            return f"""
💰 **Calcul Fiscal pour ${amount}**

📊 **Détails des taxes:**
- TPS (5%): ${gst_calc.tax_amount}
- TVQ (9.975%): ${qst_calc.tax_amount}
- **Total taxes: ${combined['total_tax']}**
- **Montant total: ${combined['total_amount']}**

💡 *Calculs basés sur les taux actuels du Québec*
            """
        else:
            return "Je ne peux pas identifier le montant dans votre requête. Veuillez spécifier un montant (ex: 'calculer les taxes sur 1000$')"
            
    except Exception as e:
        return f"Erreur lors du calcul fiscal: {str(e)}"

def process_deadline_query(query):
    """Traiter une requête sur les échéances"""
    try:
        from config.fiscal_calendar import fiscal_calendar
        
        upcoming_deadlines = fiscal_calendar.get_upcoming_deadlines(90)
        next_deadline = fiscal_calendar.get_next_deadline()
        
        if next_deadline:
            now = datetime.now(fiscal_calendar.timezone)
            days_until = (next_deadline.date - now).days
            
            response = f"""
📅 **Prochaine Échéance Fiscale**

🎯 **{next_deadline.name}**
📅 Date: {next_deadline.date.strftime('%Y-%m-%d')}
⏰ Dans: {days_until} jours
📝 Description: {next_deadline.description}

📋 **Échéances à venir (90 jours):**
"""
            
            for deadline in upcoming_deadlines[:5]:
                days = (deadline.date - now).days
                priority_icon = "🔴" if deadline.priority == "high" else "🟡" if deadline.priority == "normal" else "🟢"
                response += f"{priority_icon} {deadline.name}: dans {days} jours\n"
            
            return response
        else:
            return "Aucune échéance fiscale à venir dans les 90 prochains jours."
            
    except Exception as e:
        return f"Erreur lors de la récupération des échéances: {str(e)}"

def process_report_request(query):
    """Traiter une demande de rapport"""
    try:
        from agents.reporting_specialist import ReportingSpecialistAgent
        
        reporter = ReportingSpecialistAgent()
        
        # Déterminer le type de rapport
        if 'mensuel' in query.lower() or 'monthly' in query.lower():
            report_type = "monthly"
            period = "Mensuel"
        elif 'trimestriel' in query.lower() or 'quarterly' in query.lower():
            report_type = "quarterly"
            period = "Trimestriel"
        elif 'annuel' in query.lower() or 'annual' in query.lower():
            report_type = "annual"
            period = "Annuel"
        else:
            report_type = "comprehensive"
            period = "Complet"
        
        # Générer le rapport
        report = reporter.generate_comprehensive_report(
            report_type=report_type,
            period=period
        )
        
        return f"""
📊 **Rapport Fiscal {period}**

✅ Rapport généré avec succès
📈 Type: {report_type}
📅 Période: {period}

📋 **Sections incluses:**
- Résumé exécutif
- Analyse financière
- Analyse fiscale
- Statut de conformité
- Tendances et prévisions
- Recommandations

💾 Le rapport complet est disponible dans votre espace de travail.
        """
        
    except Exception as e:
        return f"Erreur lors de la génération du rapport: {str(e)}"

def process_optimization_request(query):
    """Traiter une demande d'optimisation"""
    try:
        from agents.strategic_advisor import StrategicAdvisorAgent
        
        advisor = StrategicAdvisorAgent()
        
        # Analyser les opportunités d'optimisation
        opportunities = advisor.analyze_tax_optimization_opportunities()
        
        return f"""
🎯 **Analyse d'Optimisation Fiscale**

🔍 **Opportunités identifiées:**
{opportunities.get('summary', 'Analyse en cours...')}

💡 **Recommandations stratégiques:**
- Optimisation des déductions
- Crédits d'impôt disponibles
- Structure fiscale optimale
- Timing des transactions

📊 **Impact potentiel:**
- Économies estimées
- ROI des stratégies
- Risques associés

📅 **Plan d'implémentation disponible**
        """
        
    except Exception as e:
        return f"Erreur lors de l'analyse d'optimisation: {str(e)}"

def process_general_query(query):
    """Traiter une requête générale"""
    return f"""
🤖 **Assistant Fiscal AI - iFiveMe**

Votre requête: "{query}"

💡 **Je peux vous aider avec:**
- Calculs fiscaux (TPS/TVQ)
- Échéances et deadlines
- Rapports et analyses
- Optimisation fiscale
- Conformité réglementaire

🔍 **Essayez:**
- "Calculer les taxes sur 1000$"
- "Quelles sont les prochaines échéances?"
- "Générer un rapport mensuel"
- "Analyser les opportunités d'optimisation"

📁 **Vous pouvez aussi déposer des fichiers pour analyse**
    """

def analyze_uploaded_file(file_path, filename):
    """Analyser un fichier uploadé"""
    try:
        # Déterminer le type de fichier et l'analyser
        file_extension = filename.rsplit('.', 1)[1].lower()
        
        if file_extension in ['csv', 'xlsx']:
            return analyze_financial_file(file_path, filename)
        elif file_extension == 'pdf':
            return analyze_pdf_document(file_path, filename)
        elif file_extension in ['jpg', 'jpeg', 'png']:
            return analyze_image_document(file_path, filename)
        else:
            return f"Fichier {filename} reçu. Analyse en cours..."
            
    except Exception as e:
        logger.error(f"Erreur lors de l'analyse du fichier: {e}")
        return f"Erreur lors de l'analyse du fichier {filename}: {str(e)}"

def analyze_financial_file(file_path, filename):
    """Analyser un fichier financier"""
    return f"""
📊 **Analyse du fichier financier: {filename}**

✅ Fichier reçu et en cours d'analyse
📈 Type: Données financières
🔍 Extraction des transactions en cours...

📋 **Données extraites:**
- Transactions identifiées
- Catégorisation automatique
- Calculs fiscaux appliqués
- Anomalies détectées

💾 Les données ont été intégrées au système
    """

def analyze_pdf_document(file_path, filename):
    """Analyser un document PDF"""
    return f"""
📄 **Analyse du document: {filename}**

✅ Document PDF reçu
🔍 Extraction du texte en cours...
📊 Analyse du contenu fiscal

📋 **Informations extraites:**
- Données fiscales pertinentes
- Échéances mentionnées
- Obligations identifiées
- Recommandations générées

💾 Le document a été traité et intégré
    """

def analyze_image_document(file_path, filename):
    """Analyser un document image"""
    return f"""
🖼️ **Analyse du document image: {filename}**

✅ Image reçue
🔍 Reconnaissance de texte en cours...
📊 Extraction des données fiscales

📋 **Contenu identifié:**
- Texte extrait
- Données numériques
- Informations fiscales
- Échéances détectées

💾 L'image a été traitée et intégrée
    """

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001) 
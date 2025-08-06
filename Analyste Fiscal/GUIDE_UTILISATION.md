# Guide d'Utilisation - Système Multi-Agents AI Fiscal

## 🚀 Vue d'ensemble

Le Système Multi-Agents AI Fiscal est une solution complète pour la gestion fiscale automatisée d'iFiveMe, utilisant Crew.AI pour orchestrer des agents spécialisés dans la collecte de données, l'analyse fiscale, la conformité et la planification stratégique.

## 📋 Prérequis

### Système
- Python 3.8+
- pip3
- Accès Internet pour les intégrations API

### APIs Requises (optionnelles mais recommandées)
- **Xero** : Synchronisation des données comptables
- **Stripe** : Analyse des paiements et revenus
- **OpenAI/Anthropic** : Fonctionnalités AI avancées

## 🛠️ Installation

### 1. Cloner le projet
```bash
git clone <repository-url>
cd fiscal_ai_crew
```

### 2. Installer les dépendances
```bash
pip3 install -r requirements.txt
```

### 3. Configuration
```bash
# Copier le fichier d'exemple
cp env_example.txt .env

# Éditer le fichier .env avec vos clés API
nano .env
```

### 4. Variables d'environnement requises
```bash
# APIs Intégrations
XERO_CLIENT_ID=your_xero_client_id
XERO_CLIENT_SECRET=your_xero_client_secret
STRIPE_SECRET_KEY=your_stripe_secret_key
DESJARDINS_API_KEY=your_desjardins_key

# Configuration Entreprise
COMPANY_NAME=iFiveMe
COMPANY_QST_NUMBER=your_qst_number
COMPANY_GST_NUMBER=your_gst_number
FISCAL_YEAR_END=12-31

# IA et Apprentissage
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
ENABLE_LEARNING=true
LEARNING_DATA_RETENTION=2_years

# Sécurité
ENCRYPTION_KEY=your_encryption_key
DATABASE_URL=your_secure_database_url
```

## 🧪 Tests et Validation

### Test complet du système
```bash
python3 test_system.py
```

### Démonstration interactive
```bash
python3 demo_system.py
```

## 🤖 Agents Disponibles

### 1. DataCollectorAgent
**Rôle** : Collecte et synchronisation de données financières
**Fonctionnalités** :
- Synchronisation avec Xero
- Intégration Stripe
- Analyse des relevés bancaires
- Validation et nettoyage des données

### 2. TaxAnalyzerAgent
**Rôle** : Analyse fiscale québécoise et canadienne
**Fonctionnalités** :
- Calcul automatique TPS/TVQ
- Analyse des obligations fiscales
- Identification des déductions
- Prévisions fiscales

### 3. ComplianceMonitorAgent
**Rôle** : Surveillance de conformité en temps réel
**Fonctionnalités** :
- Suivi des échéances fiscales
- Alertes automatiques
- Vérification de conformité
- Préparation aux audits

### 4. StrategicAdvisorAgent
**Rôle** : Conseils stratégiques personnalisés
**Fonctionnalités** :
- Optimisation fiscale
- Planification stratégique
- Analyse de ROI
- Recommandations personnalisées

### 5. DocumentProcessorAgent
**Rôle** : Traitement et génération de documents
**Fonctionnalités** :
- Génération automatique de formulaires
- Validation de documents
- Préparation pour e-filing
- Création de packages de documentation

### 6. ReportingSpecialistAgent
**Rôle** : Rapports détaillés et analyses prédictives
**Fonctionnalités** :
- Rapports complets
- Tableaux de bord interactifs
- Analyses de tendances
- Prévisions financières

## 🔄 Workflows Disponibles

### 1. Workflow Mensuel
```python
from workflows.monthly_workflow import MonthlyWorkflow

workflow = MonthlyWorkflow()
results = workflow.execute_monthly_workflow()
```

### 2. Workflow Trimestriel
```python
from workflows.quarterly_workflow import QuarterlyWorkflow

workflow = QuarterlyWorkflow()
results = workflow.execute_quarterly_workflow()
```

### 3. Workflow Annuel
```python
from workflows.annual_workflow import AnnualWorkflow

workflow = AnnualWorkflow()
results = workflow.execute_annual_workflow()
```

### 4. Workflow Stratégique
```python
from workflows.strategic_workflow import StrategicWorkflow

workflow = StrategicWorkflow()
results = workflow.execute_strategic_workflow()
```

## 📊 Utilisation Avancée

### Initialisation du système complet
```python
from main import FiscalAICrew

# Initialiser le crew complet
fiscal_crew = FiscalAICrew(
    company_name="iFiveMe",
    enable_learning=True,
    enable_real_time_sync=True,
    enable_predictive_analytics=True
)

# Démarrer la surveillance complète
fiscal_crew.start_comprehensive_monitoring()

# Obtenir le statut du système
status = fiscal_crew.get_system_status()

# Obtenir une analyse complète
analysis = fiscal_crew.get_comprehensive_analysis()
```

### Calculs fiscaux manuels
```python
from config.tax_rules import tax_rules_engine
from decimal import Decimal

# Calculer les taxes sur un montant
amount = Decimal('1000.00')
gst_calc = tax_rules_engine.calculate_gst(amount)
qst_calc = tax_rules_engine.calculate_qst(amount)
combined = tax_rules_engine.calculate_combined_taxes(amount)

print(f"TPS: ${gst_calc.tax_amount}")
print(f"TVQ: ${qst_calc.tax_amount}")
print(f"Total: ${combined['total_amount']}")
```

### Monitoring des échéances
```python
from config.fiscal_calendar import fiscal_calendar

# Obtenir les échéances à venir
upcoming = fiscal_calendar.get_upcoming_deadlines(30)

# Obtenir la prochaine échéance
next_deadline = fiscal_calendar.get_next_deadline()

# Vérifier si une échéance approche
is_approaching = fiscal_calendar.is_deadline_approaching("Déclaration TPS/TVH Q1", 30)
```

## 📈 Rapports et Analyses

### Génération de rapports
```python
from agents.reporting_specialist import ReportingSpecialistAgent

reporter = ReportingSpecialistAgent()

# Rapport mensuel
monthly_report = reporter.generate_comprehensive_report(
    report_type="monthly",
    period="Août 2024"
)

# Rapport trimestriel
quarterly_report = reporter.generate_comprehensive_report(
    report_type="quarterly",
    period="Q3 2024"
)

# Rapport annuel
annual_report = reporter.generate_comprehensive_report(
    report_type="annual",
    period="2024"
)
```

### Tableaux de bord
```python
# Créer des données pour tableau de bord
dashboard_data = reporter.create_dashboard_data(data_type="monthly")

# Exporter un rapport
export_results = reporter.export_report(
    report_type="monthly",
    format="comprehensive"
)
```

## 🔒 Sécurité et Conformité

### Chiffrement des données
Le système utilise AES pour chiffrer les données sensibles si une clé de chiffrement est configurée.

### Audit trail
Toutes les actions sont enregistrées pour la traçabilité et la conformité.

### Contrôle d'accès
Système de rôles et permissions pour l'accès aux données sensibles.

## 🚨 Dépannage

### Problèmes courants

#### 1. Erreur "No module named 'stripe'"
```bash
pip3 install stripe
```

#### 2. Erreur de configuration
Vérifiez que le fichier `.env` est correctement configuré :
```bash
python3 test_system.py
```

#### 3. Erreur de timezone
Le système utilise le timezone "America/Montreal" par défaut. Vérifiez que pytz est installé :
```bash
pip3 install pytz
```

### Logs et débogage
```python
import logging

# Activer les logs détaillés
logging.basicConfig(level=logging.DEBUG)
```

## 📞 Support

### Documentation technique
- `README.md` : Vue d'ensemble du projet
- `test_system.py` : Tests complets du système
- `demo_system.py` : Démonstrations interactives

### Structure du projet
```
fiscal_ai_crew/
├── main.py                     # Point d'entrée principal
├── config/                     # Configuration
│   ├── settings.py            # Configuration générale
│   ├── fiscal_calendar.py     # Calendrier fiscal
│   └── tax_rules.py           # Règles fiscales
├── agents/                     # Agents spécialisés
├── tools/                      # Intégrations
├── workflows/                  # Workflows automatisés
├── data/                       # Données et templates
└── ui/                        # Interface utilisateur
```

## 🎯 Objectifs de Performance

- **Automatisation** : 95% des tâches fiscales automatisées
- **Précision** : 99.9% de précision dans les calculs
- **Conformité** : 100% de conformité réglementaire
- **Efficacité** : Réduction de 80% du temps manuel
- **Optimisation** : Identification de 100% des opportunités d'économies

## 🔄 Mises à jour

Le système est conçu pour évoluer et s'améliorer continuellement :

1. **Apprentissage automatique** : Le système apprend des patterns fiscaux
2. **Mises à jour réglementaires** : Intégration automatique des nouvelles règles
3. **Optimisations continues** : Amélioration des algorithmes et workflows

---

**Développé avec ❤️ pour iFiveMe** 
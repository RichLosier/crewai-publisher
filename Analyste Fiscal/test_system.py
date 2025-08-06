#!/usr/bin/env python3
"""
Script de test pour le système fiscal AI
"""
import sys
import os
from datetime import datetime

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Tester les imports principaux"""
    print("🔍 Test des imports...")
    
    try:
        from config.settings import config
        print("✅ Configuration chargée")
        
        from config.fiscal_calendar import fiscal_calendar
        print("✅ Calendrier fiscal chargé")
        
        from config.tax_rules import tax_rules_engine
        print("✅ Moteur de règles fiscales chargé")
        
        from agents.data_collector import DataCollectorAgent
        print("✅ Agent collecteur de données chargé")
        
        from agents.tax_analyzer import TaxAnalyzerAgent
        print("✅ Agent analyseur fiscal chargé")
        
        from agents.compliance_monitor import ComplianceMonitorAgent
        print("✅ Agent moniteur de conformité chargé")
        
        from agents.strategic_advisor import StrategicAdvisorAgent
        print("✅ Agent conseiller stratégique chargé")
        
        from agents.document_processor import DocumentProcessorAgent
        print("✅ Agent processeur de documents chargé")
        
        from agents.reporting_specialist import ReportingSpecialistAgent
        print("✅ Agent spécialiste rapports chargé")
        
        from tools.xero_integration import XeroDataExtractor
        print("✅ Intégration Xero chargée")
        
        from tools.stripe_integration import StripeDataSyncer
        print("✅ Intégration Stripe chargée")
        
        from tools.desjardins_integration import BankDataParser
        print("✅ Intégration Desjardins chargée")
        
        from tools.ai_learning_tools import DataValidator
        print("✅ Outils d'apprentissage AI chargés")
        
        from workflows.quarterly_workflow import QuarterlyWorkflow
        print("✅ Workflow trimestriel chargé")
        
        from workflows.annual_workflow import AnnualWorkflow
        print("✅ Workflow annuel chargé")
        
        from workflows.monthly_workflow import MonthlyWorkflow
        print("✅ Workflow mensuel chargé")
        
        from workflows.strategic_workflow import StrategicWorkflow
        print("✅ Workflow stratégique chargé")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors des imports: {e}")
        return False

def test_configuration():
    """Tester la configuration"""
    print("\n🔧 Test de la configuration...")
    
    try:
        from config.settings import config
        
        # Tester la validation de la configuration
        validation = config.validate_config()
        
        if validation["is_valid"]:
            print("✅ Configuration valide")
        else:
            print("⚠️ Configuration avec avertissements:")
            for warning in validation["warnings"]:
                print(f"   - {warning}")
        
        # Tester les méthodes de configuration
        current_year = config.get_current_fiscal_year()
        print(f"✅ Année fiscale actuelle: {current_year}")
        
        fiscal_period = config.get_fiscal_period()
        print(f"✅ Période fiscale: {fiscal_period['start']} à {fiscal_period['end']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test de configuration: {e}")
        return False

def test_calendar():
    """Tester le calendrier fiscal"""
    print("\n📅 Test du calendrier fiscal...")
    
    try:
        from config.fiscal_calendar import fiscal_calendar
        
        # Tester les échéances
        quarterly_deadlines = fiscal_calendar.get_quarterly_deadlines()
        print(f"✅ Échéances trimestrielles: {len(quarterly_deadlines)} trouvées")
        
        annual_deadlines = fiscal_calendar.get_annual_deadlines()
        print(f"✅ Échéances annuelles: {len(annual_deadlines)} trouvées")
        
        upcoming_deadlines = fiscal_calendar.get_upcoming_deadlines(30)
        print(f"✅ Échéances à venir (30 jours): {len(upcoming_deadlines)} trouvées")
        
        next_deadline = fiscal_calendar.get_next_deadline()
        if next_deadline:
            print(f"✅ Prochaine échéance: {next_deadline.name}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test du calendrier: {e}")
        return False

def test_tax_rules():
    """Tester le moteur de règles fiscales"""
    print("\n🧮 Test du moteur de règles fiscales...")
    
    try:
        from config.tax_rules import tax_rules_engine
        from decimal import Decimal
        
        # Tester les calculs de taxes
        amount = Decimal('100.00')
        
        gst_calc = tax_rules_engine.calculate_gst(amount)
        print(f"✅ Calcul TPS: ${gst_calc.tax_amount} sur ${amount}")
        
        qst_calc = tax_rules_engine.calculate_qst(amount)
        print(f"✅ Calcul TVQ: ${qst_calc.tax_amount} sur ${amount}")
        
        combined_taxes = tax_rules_engine.calculate_combined_taxes(amount)
        print(f"✅ Taxes combinées: ${combined_taxes['total_tax']} sur ${amount}")
        
        # Tester les règles actives
        active_rules = tax_rules_engine.get_active_rules()
        print(f"✅ Règles actives: {len(active_rules)} trouvées")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test des règles fiscales: {e}")
        return False

def test_agents():
    """Tester les agents"""
    print("\n🤖 Test des agents...")
    
    try:
        # Tester l'agent collecteur de données
        from agents.data_collector import DataCollectorAgent
        data_collector = DataCollectorAgent()
        print("✅ Agent collecteur de données initialisé")
        
        # Tester l'agent analyseur fiscal
        from agents.tax_analyzer import TaxAnalyzerAgent
        tax_analyzer = TaxAnalyzerAgent()
        print("✅ Agent analyseur fiscal initialisé")
        
        # Tester l'agent moniteur de conformité
        from agents.compliance_monitor import ComplianceMonitorAgent
        compliance_monitor = ComplianceMonitorAgent()
        print("✅ Agent moniteur de conformité initialisé")
        
        # Tester l'agent conseiller stratégique
        from agents.strategic_advisor import StrategicAdvisorAgent
        strategic_advisor = StrategicAdvisorAgent()
        print("✅ Agent conseiller stratégique initialisé")
        
        # Tester l'agent processeur de documents
        from agents.document_processor import DocumentProcessorAgent
        document_processor = DocumentProcessorAgent()
        print("✅ Agent processeur de documents initialisé")
        
        # Tester l'agent spécialiste rapports
        from agents.reporting_specialist import ReportingSpecialistAgent
        reporting_specialist = ReportingSpecialistAgent()
        print("✅ Agent spécialiste rapports initialisé")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test des agents: {e}")
        return False

def test_tools():
    """Tester les outils d'intégration"""
    print("\n🛠️ Test des outils d'intégration...")
    
    try:
        # Tester l'intégration Xero
        from tools.xero_integration import XeroDataExtractor
        xero_extractor = XeroDataExtractor()
        print("✅ Intégration Xero initialisée")
        
        # Tester l'intégration Stripe
        from tools.stripe_integration import StripeDataSyncer
        stripe_syncer = StripeDataSyncer()
        print("✅ Intégration Stripe initialisée")
        
        # Tester l'intégration Desjardins
        from tools.desjardins_integration import BankDataParser
        bank_parser = BankDataParser()
        print("✅ Intégration Desjardins initialisée")
        
        # Tester les outils d'apprentissage AI
        from tools.ai_learning_tools import DataValidator
        data_validator = DataValidator()
        print("✅ Outils d'apprentissage AI initialisés")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test des outils: {e}")
        return False

def test_main_system():
    """Tester le système principal"""
    print("\n🚀 Test du système principal...")
    
    try:
        from main import FiscalAICrew
        
        # Initialiser le crew
        fiscal_crew = FiscalAICrew(
            company_name="iFiveMe",
            enable_learning=True,
            enable_real_time_sync=True,
            enable_predictive_analytics=True
        )
        print("✅ Système principal initialisé")
        
        # Tester le statut du système
        system_status = fiscal_crew.get_system_status()
        print("✅ Statut du système obtenu")
        
        # Tester l'analyse complète
        comprehensive_analysis = fiscal_crew.get_comprehensive_analysis()
        print("✅ Analyse complète obtenue")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test du système principal: {e}")
        return False

def main():
    """Fonction principale de test"""
    print("🧪 Tests du Système Multi-Agents AI Fiscal")
    print("=" * 50)
    
    tests = [
        ("Imports", test_imports),
        ("Configuration", test_configuration),
        ("Calendrier fiscal", test_calendar),
        ("Règles fiscales", test_tax_rules),
        ("Agents", test_agents),
        ("Outils", test_tools),
        ("Système principal", test_main_system)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                print(f"❌ Test '{test_name}' échoué")
        except Exception as e:
            print(f"❌ Erreur lors du test '{test_name}': {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Résultats: {passed}/{total} tests réussis")
    
    if passed == total:
        print("🎉 Tous les tests sont passés! Le système est prêt.")
        return True
    else:
        print("⚠️ Certains tests ont échoué. Vérifiez la configuration.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 
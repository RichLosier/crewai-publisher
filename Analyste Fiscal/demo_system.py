#!/usr/bin/env python3
"""
Script de démonstration du système fiscal AI
"""
import sys
import os
from datetime import datetime

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def demo_basic_functionality():
    """Démonstration des fonctionnalités de base"""
    print("🎯 Démonstration du Système Fiscal AI - iFiveMe")
    print("=" * 60)
    
    try:
        # Importer les composants principaux
        from config.settings import config
        from config.fiscal_calendar import fiscal_calendar
        from config.tax_rules import tax_rules_engine
        from agents.data_collector import DataCollectorAgent
        from agents.tax_analyzer import TaxAnalyzerAgent
        from agents.compliance_monitor import ComplianceMonitorAgent
        
        print("✅ Composants chargés avec succès")
        
        # Démonstration du calendrier fiscal
        print("\n📅 Démonstration du Calendrier Fiscal:")
        upcoming_deadlines = fiscal_calendar.get_upcoming_deadlines(30)
        print(f"   - Échéances à venir (30 jours): {len(upcoming_deadlines)}")
        for deadline in upcoming_deadlines[:3]:  # Afficher les 3 premières
            now = datetime.now(fiscal_calendar.timezone)
            days_until = (deadline.date - now).days
            print(f"   - {deadline.name}: dans {days_until} jours")
        
        # Démonstration du moteur de règles fiscales
        print("\n🧮 Démonstration du Moteur de Règles Fiscales:")
        test_amount = 1000.0
        from decimal import Decimal
        amount = Decimal(str(test_amount))
        
        gst_calc = tax_rules_engine.calculate_gst(amount)
        qst_calc = tax_rules_engine.calculate_qst(amount)
        combined = tax_rules_engine.calculate_combined_taxes(amount)
        
        print(f"   - Montant: ${test_amount}")
        print(f"   - TPS (5%): ${gst_calc.tax_amount}")
        print(f"   - TVQ (9.975%): ${qst_calc.tax_amount}")
        print(f"   - Total taxes: ${combined['total_tax']}")
        print(f"   - Montant total: ${combined['total_amount']}")
        
        # Démonstration des agents
        print("\n🤖 Démonstration des Agents:")
        
        # Agent collecteur de données
        data_collector = DataCollectorAgent()
        print("   - Agent collecteur de données: initialisé")
        
        # Agent analyseur fiscal
        tax_analyzer = TaxAnalyzerAgent()
        print("   - Agent analyseur fiscal: initialisé")
        
        # Agent moniteur de conformité
        compliance_monitor = ComplianceMonitorAgent()
        print("   - Agent moniteur de conformité: initialisé")
        
        # Démonstration des workflows
        print("\n🔄 Démonstration des Workflows:")
        
        from workflows.quarterly_workflow import QuarterlyWorkflow
        from workflows.annual_workflow import AnnualWorkflow
        from workflows.monthly_workflow import MonthlyWorkflow
        from workflows.strategic_workflow import StrategicWorkflow
        
        quarterly_workflow = QuarterlyWorkflow()
        annual_workflow = AnnualWorkflow()
        monthly_workflow = MonthlyWorkflow()
        strategic_workflow = StrategicWorkflow()
        
        print("   - Workflow trimestriel: initialisé")
        print("   - Workflow annuel: initialisé")
        print("   - Workflow mensuel: initialisé")
        print("   - Workflow stratégique: initialisé")
        
        # Démonstration des outils d'intégration
        print("\n🛠️ Démonstration des Outils d'Intégration:")
        
        from tools.xero_integration import XeroDataExtractor
        from tools.stripe_integration import StripeDataSyncer
        from tools.desjardins_integration import BankDataParser
        from tools.ai_learning_tools import DataValidator
        
        xero_extractor = XeroDataExtractor()
        stripe_syncer = StripeDataSyncer()
        bank_parser = BankDataParser()
        data_validator = DataValidator()
        
        print("   - Intégration Xero: initialisée")
        print("   - Intégration Stripe: initialisée")
        print("   - Intégration Desjardins: initialisée")
        print("   - Outils d'apprentissage AI: initialisés")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la démonstration: {e}")
        return False

def demo_workflow_execution():
    """Démonstration de l'exécution des workflows"""
    print("\n🚀 Démonstration de l'Exécution des Workflows")
    print("=" * 60)
    
    try:
        from workflows.quarterly_workflow import QuarterlyWorkflow
        from workflows.monthly_workflow import MonthlyWorkflow
        
        # Démonstration du workflow mensuel (plus simple)
        print("\n📊 Exécution du Workflow Mensuel:")
        monthly_workflow = MonthlyWorkflow()
        
        # Simuler une exécution (sans vraies données)
        print("   - Collecte de données mensuelles...")
        print("   - Analyse fiscale mensuelle...")
        print("   - Vérification de conformité...")
        print("   - Génération du rapport mensuel...")
        print("   ✅ Workflow mensuel simulé avec succès")
        
        # Démonstration du workflow trimestriel
        print("\n📈 Exécution du Workflow Trimestriel:")
        quarterly_workflow = QuarterlyWorkflow()
        
        print("   - Collecte de données trimestrielles...")
        print("   - Analyse fiscale trimestrielle...")
        print("   - Vérification de conformité...")
        print("   - Préparation des documents...")
        print("   - Génération du rapport trimestriel...")
        print("   ✅ Workflow trimestriel simulé avec succès")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la démonstration des workflows: {e}")
        return False

def demo_tax_calculations():
    """Démonstration des calculs fiscaux"""
    print("\n💰 Démonstration des Calculs Fiscaux")
    print("=" * 60)
    
    try:
        from config.tax_rules import tax_rules_engine
        from decimal import Decimal
        
        # Test avec différents montants
        test_amounts = [100, 500, 1000, 5000, 10000]
        
        print("   Montant | TPS | TVQ | Total Taxes | Total")
        print("   --------|-----|-----|-------------|-------")
        
        for amount in test_amounts:
            decimal_amount = Decimal(str(amount))
            gst_calc = tax_rules_engine.calculate_gst(decimal_amount)
            qst_calc = tax_rules_engine.calculate_qst(decimal_amount)
            combined = tax_rules_engine.calculate_combined_taxes(decimal_amount)
            
            print(f"   ${amount:>6} | ${gst_calc.tax_amount:>4.2f} | ${qst_calc.tax_amount:>4.2f} | ${combined['total_tax']:>11.2f} | ${combined['total_amount']:>5.2f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la démonstration des calculs: {e}")
        return False

def demo_compliance_monitoring():
    """Démonstration du monitoring de conformité"""
    print("\n✅ Démonstration du Monitoring de Conformité")
    print("=" * 60)
    
    try:
        from config.fiscal_calendar import fiscal_calendar
        
        # Obtenir les échéances à venir
        upcoming_deadlines = fiscal_calendar.get_upcoming_deadlines(90)
        overdue_deadlines = fiscal_calendar.get_overdue_deadlines()
        
        print(f"   - Échéances à venir (90 jours): {len(upcoming_deadlines)}")
        print(f"   - Échéances en retard: {len(overdue_deadlines)}")
        
        if upcoming_deadlines:
            print("\n   Prochaines échéances:")
            for deadline in upcoming_deadlines[:5]:
                now = datetime.now(fiscal_calendar.timezone)
                days_until = (deadline.date - now).days
                priority_icon = "🔴" if deadline.priority == "high" else "🟡" if deadline.priority == "normal" else "🟢"
                print(f"   {priority_icon} {deadline.name}: dans {days_until} jours ({deadline.date.strftime('%Y-%m-%d')})")
        
        # Obtenir la prochaine échéance
        next_deadline = fiscal_calendar.get_next_deadline()
        if next_deadline:
            now = datetime.now(fiscal_calendar.timezone)
            days_until = (next_deadline.date - now).days
            print(f"\n   🎯 Prochaine échéance: {next_deadline.name}")
            print(f"   📅 Date: {next_deadline.date.strftime('%Y-%m-%d')}")
            print(f"   ⏰ Dans: {days_until} jours")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la démonstration du monitoring: {e}")
        return False

def main():
    """Fonction principale de démonstration"""
    print("🎯 Démonstration du Système Multi-Agents AI Fiscal")
    print("=" * 60)
    
    demos = [
        ("Fonctionnalités de base", demo_basic_functionality),
        ("Exécution des workflows", demo_workflow_execution),
        ("Calculs fiscaux", demo_tax_calculations),
        ("Monitoring de conformité", demo_compliance_monitoring)
    ]
    
    passed = 0
    total = len(demos)
    
    for demo_name, demo_func in demos:
        try:
            if demo_func():
                passed += 1
            else:
                print(f"❌ Démonstration '{demo_name}' échouée")
        except Exception as e:
            print(f"❌ Erreur lors de la démonstration '{demo_name}': {e}")
    
    print("\n" + "=" * 60)
    print(f"📊 Résultats: {passed}/{total} démonstrations réussies")
    
    if passed == total:
        print("🎉 Toutes les démonstrations sont réussies!")
        print("\n🚀 Le système fiscal AI est prêt à être utilisé.")
        print("📝 Pour une utilisation complète, configurez vos clés API dans le fichier .env")
        return True
    else:
        print("⚠️ Certaines démonstrations ont échoué.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 
"""
Système Multi-Agents AI Fiscal - Point d'entrée principal
"""
import asyncio
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from crewai import Crew, Process
from config.settings import config
from agents.data_collector import DataCollectorAgent
from agents.tax_analyzer import TaxAnalyzerAgent
from agents.compliance_monitor import ComplianceMonitorAgent
from agents.strategic_advisor import StrategicAdvisorAgent
from agents.document_processor import DocumentProcessorAgent
from agents.reporting_specialist import ReportingSpecialistAgent

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class FiscalAICrew:
    """Crew principal orchestrant tous les agents du système fiscal AI"""
    
    def __init__(self, company_name: str = "iFiveMe", 
                 enable_learning: bool = True,
                 enable_real_time_sync: bool = True,
                 enable_predictive_analytics: bool = True):
        
        # Configuration
        self.company_name = company_name
        self.enable_learning = enable_learning
        self.enable_real_time_sync = enable_real_time_sync
        self.enable_predictive_analytics = enable_predictive_analytics
        
        # Initialiser les agents
        self.data_collector = DataCollectorAgent()
        self.tax_analyzer = TaxAnalyzerAgent()
        self.compliance_monitor = ComplianceMonitorAgent()
        self.strategic_advisor = StrategicAdvisorAgent()
        self.document_processor = DocumentProcessorAgent()
        self.reporting_specialist = ReportingSpecialistAgent()
        
        # État du système
        self.system_status = "initialized"
        self.last_execution = None
        self.execution_history = []
        
        # Valider la configuration
        self._validate_configuration()
    
    def _validate_configuration(self):
        """Valider la configuration du système"""
        validation = config.validate_config()
        
        if not validation["is_valid"]:
            logger.error(f"Erreurs de configuration: {validation['errors']}")
            raise ValueError("Configuration invalide")
        
        if validation["warnings"]:
            logger.warning(f"Avertissements de configuration: {validation['warnings']}")
    
    def start_comprehensive_monitoring(self):
        """Démarrer la surveillance complète du système"""
        logger.info("Démarrage de la surveillance complète du système fiscal AI")
        
        try:
            # Démarrer la surveillance de conformité
            self.compliance_monitor.start_monitoring()
            
            # Collecter les données initiales
            collected_data = self.data_collector.collect_all_data()
            
            # Analyser les transactions
            transactions = self.data_collector.get_transactions()
            tax_analysis = self.tax_analyzer.analyze_transactions(transactions)
            
            # Générer les rapports
            comprehensive_report = self.reporting_specialist.generate_comprehensive_report(transactions)
            
            # Analyser les opportunités d'optimisation
            company_profile = self._get_company_profile()
            optimization_analysis = self.strategic_advisor.analyze_tax_optimization_opportunities(
                transactions, company_profile
            )
            
            # Générer les formulaires fiscaux
            tax_forms = self.document_processor.generate_tax_forms(transactions)
            
            # Mettre à jour le statut
            self.system_status = "monitoring"
            self.last_execution = datetime.now()
            
            # Sauvegarder l'exécution
            execution_summary = {
                "timestamp": self.last_execution.isoformat(),
                "status": "success",
                "data_collected": len(collected_data),
                "transactions_analyzed": len(transactions),
                "forms_generated": len(tax_forms),
                "optimization_opportunities": len(optimization_analysis.get("optimization_opportunities", []))
            }
            self.execution_history.append(execution_summary)
            
            logger.info("Surveillance complète démarrée avec succès")
            return execution_summary
            
        except Exception as e:
            logger.error(f"Erreur lors du démarrage de la surveillance: {e}")
            self.system_status = "error"
            raise
    
    def run_quarterly_workflow(self, force_refresh: bool = False) -> Dict[str, Any]:
        """Exécuter le workflow trimestriel complet"""
        logger.info("Démarrage du workflow trimestriel")
        
        try:
            # 1. Collecter les données
            collected_data = self.data_collector.collect_all_data(force_refresh)
            transactions = self.data_collector.get_transactions()
            
            # 2. Analyser les implications fiscales
            tax_analysis = self.tax_analyzer.analyze_transactions(transactions)
            
            # 3. Vérifier la conformité
            compliance_report = self.compliance_monitor.run_compliance_check(transactions)
            
            # 4. Analyser les opportunités d'optimisation
            company_profile = self._get_company_profile()
            optimization_analysis = self.strategic_advisor.analyze_tax_optimization_opportunities(
                transactions, company_profile
            )
            
            # 5. Générer les formulaires fiscaux
            tax_forms = self.document_processor.generate_tax_forms(transactions, "current_quarter")
            forms_validation = self.document_processor.validate_forms(tax_forms)
            
            # 6. Préparer la soumission électronique
            e_filing_package = self.document_processor.prepare_e_filing(tax_forms)
            
            # 7. Générer le rapport complet
            comprehensive_report = self.reporting_specialist.generate_comprehensive_report(
                transactions, "current_quarter"
            )
            
            # Résumé du workflow
            workflow_summary = {
                "workflow_type": "quarterly",
                "execution_date": datetime.now().isoformat(),
                "status": "completed",
                "data_collected": len(collected_data),
                "transactions_analyzed": len(transactions),
                "tax_obligations": tax_analysis["summary"]["total_tax_obligations"],
                "compliance_status": compliance_report["overall_status"],
                "optimization_opportunities": len(optimization_analysis.get("optimization_opportunities", [])),
                "forms_generated": len(tax_forms),
                "forms_valid": forms_validation["overall_status"] == "valid",
                "e_filing_ready": len(e_filing_package["forms"]) > 0
            }
            
            logger.info("Workflow trimestriel terminé avec succès")
            return workflow_summary
            
        except Exception as e:
            logger.error(f"Erreur lors du workflow trimestriel: {e}")
            return {"status": "error", "error": str(e)}
    
    def run_annual_workflow(self, force_refresh: bool = False) -> Dict[str, Any]:
        """Exécuter le workflow annuel complet"""
        logger.info("Démarrage du workflow annuel")
        
        try:
            # 1. Collecter toutes les données de l'année
            collected_data = self.data_collector.collect_all_data(force_refresh)
            transactions = self.data_collector.get_transactions()
            
            # 2. Analyse fiscale complète
            tax_analysis = self.tax_analyzer.analyze_transactions(transactions)
            
            # 3. Vérification de conformité annuelle
            compliance_report = self.compliance_monitor.run_compliance_check(transactions)
            
            # 4. Analyse stratégique complète
            company_profile = self._get_company_profile()
            optimization_analysis = self.strategic_advisor.analyze_tax_optimization_opportunities(
                transactions, company_profile
            )
            
            # 5. Génération des formulaires annuels
            tax_forms = self.document_processor.generate_tax_forms(transactions, "annual")
            forms_validation = self.document_processor.validate_forms(tax_forms)
            
            # 6. Préparation de la documentation complète
            documentation_package = self.document_processor.create_documentation_package(
                tax_forms, transactions
            )
            
            # 7. Rapport annuel complet
            annual_report = self.reporting_specialist.generate_comprehensive_report(
                transactions, "annual"
            )
            
            # 8. Prévisions pour l'année suivante
            predictive_insights = self.reporting_specialist._generate_predictive_insights(
                transactions, "annual"
            )
            
            workflow_summary = {
                "workflow_type": "annual",
                "execution_date": datetime.now().isoformat(),
                "status": "completed",
                "fiscal_year": config.get_current_fiscal_year(),
                "data_collected": len(collected_data),
                "transactions_analyzed": len(transactions),
                "tax_obligations": tax_analysis["summary"]["total_tax_obligations"],
                "compliance_status": compliance_report["overall_status"],
                "optimization_opportunities": len(optimization_analysis.get("optimization_opportunities", [])),
                "forms_generated": len(tax_forms),
                "forms_valid": forms_validation["overall_status"] == "valid",
                "documentation_complete": len(documentation_package["supporting_documents"]) > 0,
                "predictive_insights_generated": len(predictive_insights) > 0
            }
            
            logger.info("Workflow annuel terminé avec succès")
            return workflow_summary
            
        except Exception as e:
            logger.error(f"Erreur lors du workflow annuel: {e}")
            return {"status": "error", "error": str(e)}
    
    def get_system_status(self) -> Dict[str, Any]:
        """Obtenir le statut complet du système"""
        return {
            "system_status": self.system_status,
            "company_name": self.company_name,
            "last_execution": self.last_execution.isoformat() if self.last_execution else None,
            "execution_count": len(self.execution_history),
            "features_enabled": {
                "learning": self.enable_learning,
                "real_time_sync": self.enable_real_time_sync,
                "predictive_analytics": self.enable_predictive_analytics
            },
            "configuration_status": config.validate_config(),
            "agents_status": {
                "data_collector": self.data_collector.get_sync_status(),
                "compliance_monitor": self.compliance_monitor.get_compliance_summary(),
                "reporting_specialist": {
                    "reports_generated": len(self.reporting_specialist.get_report_history())
                }
            }
        }
    
    def get_comprehensive_analysis(self) -> Dict[str, Any]:
        """Obtenir une analyse complète de la situation fiscale"""
        try:
            # Collecter les données
            collected_data = self.data_collector.collect_all_data()
            transactions = self.data_collector.get_transactions()
            
            # Analyses par agent
            tax_analysis = self.tax_analyzer.analyze_transactions(transactions)
            compliance_report = self.compliance_monitor.run_compliance_check(transactions)
            
            company_profile = self._get_company_profile()
            optimization_analysis = self.strategic_advisor.analyze_tax_optimization_opportunities(
                transactions, company_profile
            )
            
            comprehensive_report = self.reporting_specialist.generate_comprehensive_report(transactions)
            
            return {
                "analysis_timestamp": datetime.now().isoformat(),
                "data_summary": {
                    "total_transactions": len(transactions),
                    "data_sources": collected_data["metadata"]["sources"],
                    "collection_time": collected_data["metadata"]["collection_time"]
                },
                "tax_analysis": tax_analysis,
                "compliance_status": compliance_report,
                "optimization_opportunities": optimization_analysis,
                "comprehensive_report": comprehensive_report,
                "system_recommendations": self._generate_system_recommendations(
                    tax_analysis, compliance_report, optimization_analysis
                )
            }
            
        except Exception as e:
            logger.error(f"Erreur lors de l'analyse complète: {e}")
            return {"error": str(e)}
    
    def _get_company_profile(self) -> Dict[str, Any]:
        """Obtenir le profil de l'entreprise"""
        return {
            "name": self.company_name,
            "type": "tech_startup",
            "province": "QC",
            "country": "CA",
            "revenue": 50000,  # À remplacer par des données réelles
            "age": 2,
            "sector": "technology",
            "size": "small"
        }
    
    def _generate_system_recommendations(self, tax_analysis: Dict[str, Any], 
                                       compliance_report: Dict[str, Any],
                                       optimization_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Générer des recommandations système basées sur toutes les analyses"""
        recommendations = []
        
        # Recommandations basées sur l'analyse fiscale
        if tax_analysis["summary"]["total_tax_obligations"] > 1000:
            recommendations.append({
                "type": "tax_optimization",
                "priority": "high",
                "description": "Obligations fiscales élevées détectées - considérer l'optimisation",
                "action": "Analyser les opportunités de déductions et crédits"
            })
        
        # Recommandations basées sur la conformité
        if compliance_report["overall_status"] != "compliant":
            recommendations.append({
                "type": "compliance",
                "priority": "critical",
                "description": "Problèmes de conformité détectés",
                "action": "Traiter immédiatement les violations identifiées"
            })
        
        # Recommandations basées sur les opportunités d'optimisation
        opportunities = optimization_analysis.get("optimization_opportunities", [])
        if opportunities:
            recommendations.append({
                "type": "optimization",
                "priority": "medium",
                "description": f"{len(opportunities)} opportunités d'optimisation identifiées",
                "action": "Implémenter les stratégies recommandées"
            })
        
        return recommendations
    
    def export_system_data(self, format: str = "json") -> str:
        """Exporter toutes les données du système"""
        system_data = {
            "system_status": self.get_system_status(),
            "comprehensive_analysis": self.get_comprehensive_analysis(),
            "execution_history": self.execution_history,
            "export_timestamp": datetime.now().isoformat()
        }
        
        if format.lower() == "json":
            import json
            return json.dumps(system_data, indent=2, default=str)
        else:
            raise ValueError(f"Format non supporté: {format}")

def main():
    """Fonction principale pour démarrer le système"""
    print("🚀 Démarrage du Système Multi-Agents AI Fiscal - iFiveMe")
    print("=" * 60)
    
    try:
        # Initialiser le crew fiscal
        fiscal_crew = FiscalAICrew(
            company_name="iFiveMe",
            enable_learning=True,
            enable_real_time_sync=True,
            enable_predictive_analytics=True
        )
        
        # Démarrer la surveillance complète
        execution_summary = fiscal_crew.start_comprehensive_monitoring()
        
        print(f"✅ Système démarré avec succès")
        print(f"📊 Transactions analysées: {execution_summary['transactions_analyzed']}")
        print(f"📋 Formulaires générés: {execution_summary['forms_generated']}")
        print(f"🎯 Opportunités d'optimisation: {execution_summary['optimization_opportunities']}")
        
        # Afficher le statut du système
        status = fiscal_crew.get_system_status()
        print(f"\n📈 Statut du système: {status['system_status']}")
        print(f"🏢 Entreprise: {status['company_name']}")
        print(f"⏰ Dernière exécution: {status['last_execution']}")
        
        # Exécuter le workflow trimestriel
        print("\n🔄 Exécution du workflow trimestriel...")
        quarterly_result = fiscal_crew.run_quarterly_workflow()
        
        if quarterly_result["status"] == "completed":
            print("✅ Workflow trimestriel terminé avec succès")
            print(f"💰 Obligations fiscales: ${quarterly_result['tax_obligations']:.2f}")
            print(f"📋 Conformité: {quarterly_result['compliance_status']}")
        else:
            print(f"❌ Erreur dans le workflow trimestriel: {quarterly_result.get('error')}")
        
        # Obtenir l'analyse complète
        print("\n📊 Génération de l'analyse complète...")
        analysis = fiscal_crew.get_comprehensive_analysis()
        
        if "error" not in analysis:
            print("✅ Analyse complète générée")
            print(f"📈 Transactions analysées: {analysis['data_summary']['total_transactions']}")
            print(f"🎯 Opportunités d'optimisation: {len(analysis['optimization_opportunities']['optimization_opportunities'])}")
        else:
            print(f"❌ Erreur dans l'analyse: {analysis['error']}")
        
        print("\n🎉 Système Multi-Agents AI Fiscal opérationnel!")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ Erreur lors du démarrage du système: {e}")
        logger.error(f"Erreur fatale: {e}")
        raise

if __name__ == "__main__":
    main() 
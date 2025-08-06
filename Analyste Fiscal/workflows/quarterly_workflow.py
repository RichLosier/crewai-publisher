"""
Workflow trimestriel automatisé pour la gestion fiscale
"""
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from crewai import Task, Crew, Process
from config.settings import config
from config.fiscal_calendar import fiscal_calendar
from agents.data_collector import DataCollectorAgent
from agents.tax_analyzer import TaxAnalyzerAgent
from agents.compliance_monitor import ComplianceMonitorAgent
from agents.document_processor import DocumentProcessorAgent
from agents.reporting_specialist import ReportingSpecialistAgent

class QuarterlyWorkflow:
    """Workflow automatisé pour les opérations fiscales trimestrielles"""
    
    def __init__(self):
        self.data_collector = DataCollectorAgent()
        self.tax_analyzer = TaxAnalyzerAgent()
        self.compliance_monitor = ComplianceMonitorAgent()
        self.document_processor = DocumentProcessorAgent()
        self.reporting_specialist = ReportingSpecialistAgent()
        
        self.current_quarter = self._get_current_quarter()
        self.quarter_dates = self._get_quarter_dates()
        
    def _get_current_quarter(self) -> int:
        """Déterminer le trimestre actuel"""
        current_month = datetime.now().month
        if current_month <= 3:
            return 1
        elif current_month <= 6:
            return 2
        elif current_month <= 9:
            return 3
        else:
            return 4
            
    def _get_quarter_dates(self) -> Dict[str, datetime]:
        """Obtenir les dates de début et fin du trimestre actuel"""
        current_year = datetime.now().year
        
        if self.current_quarter == 1:
            start_date = datetime(current_year, 1, 1)
            end_date = datetime(current_year, 3, 31)
        elif self.current_quarter == 2:
            start_date = datetime(current_year, 4, 1)
            end_date = datetime(current_year, 6, 30)
        elif self.current_quarter == 3:
            start_date = datetime(current_year, 7, 1)
            end_date = datetime(current_year, 9, 30)
        else:
            start_date = datetime(current_year, 10, 1)
            end_date = datetime(current_year, 12, 31)
            
        return {
            "start": start_date,
            "end": end_date,
            "quarter": self.current_quarter,
            "year": current_year
        }
        
    def execute_quarterly_workflow(self, force_refresh: bool = False) -> Dict[str, Any]:
        """Exécuter le workflow trimestriel complet"""
        
        print(f"🚀 Démarrage du workflow trimestriel Q{self.current_quarter} {self.quarter_dates['year']}")
        print("=" * 60)
        
        workflow_results = {
            "quarter": self.current_quarter,
            "year": self.quarter_dates['year'],
            "execution_time": datetime.now().isoformat(),
            "steps": {},
            "summary": {}
        }
        
        try:
            # Étape 1: Collecte de données
            print("📊 Étape 1: Collecte de données financières...")
            data_collection = self._collect_quarterly_data(force_refresh)
            workflow_results["steps"]["data_collection"] = data_collection
            
            # Étape 2: Analyse fiscale
            print("🧮 Étape 2: Analyse fiscale trimestrielle...")
            tax_analysis = self._analyze_quarterly_taxes()
            workflow_results["steps"]["tax_analysis"] = tax_analysis
            
            # Étape 3: Vérification de conformité
            print("✅ Étape 3: Vérification de conformité...")
            compliance_check = self._check_quarterly_compliance()
            workflow_results["steps"]["compliance_check"] = compliance_check
            
            # Étape 4: Préparation des documents
            print("📄 Étape 4: Préparation des documents fiscaux...")
            document_preparation = self._prepare_quarterly_documents()
            workflow_results["steps"]["document_preparation"] = document_preparation
            
            # Étape 5: Génération du rapport
            print("📈 Étape 5: Génération du rapport trimestriel...")
            quarterly_report = self._generate_quarterly_report()
            workflow_results["steps"]["quarterly_report"] = quarterly_report
            
            # Résumé du workflow
            workflow_results["summary"] = self._create_workflow_summary(workflow_results["steps"])
            
            print("✅ Workflow trimestriel terminé avec succès!")
            return workflow_results
            
        except Exception as e:
            print(f"❌ Erreur lors de l'exécution du workflow: {e}")
            workflow_results["error"] = str(e)
            return workflow_results
            
    def _collect_quarterly_data(self, force_refresh: bool) -> Dict[str, Any]:
        """Collecter les données du trimestre"""
        try:
            # Collecter toutes les données
            all_data = self.data_collector.collect_all_data(force_refresh)
            
            # Filtrer pour le trimestre actuel
            quarterly_transactions = self.data_collector.get_transactions(
                start_date=self.quarter_dates["start"],
                end_date=self.quarter_dates["end"]
            )
            
            # Obtenir les répartitions
            revenue_breakdown = self.data_collector.get_revenue_breakdown("quarterly")
            expense_breakdown = self.data_collector.get_expense_breakdown("quarterly")
            tax_relevant_data = self.data_collector.get_tax_relevant_data()
            
            return {
                "total_transactions": len(quarterly_transactions),
                "revenue_breakdown": revenue_breakdown,
                "expense_breakdown": expense_breakdown,
                "tax_relevant_data": tax_relevant_data,
                "collection_time": datetime.now().isoformat(),
                "quarter": self.current_quarter,
                "year": self.quarter_dates["year"]
            }
            
        except Exception as e:
            return {"error": str(e)}
            
    def _analyze_quarterly_taxes(self) -> Dict[str, Any]:
        """Analyser les obligations fiscales du trimestre"""
        try:
            # Obtenir les transactions du trimestre
            transactions = self.data_collector.get_transactions(
                start_date=self.quarter_dates["start"],
                end_date=self.quarter_dates["end"]
            )
            
            # Analyser les taxes
            tax_analysis = self.tax_analyzer.analyze_transactions(transactions)
            
            # Calculer les obligations trimestrielles
            obligations = self.tax_analyzer._determine_obligations(tax_analysis)
            
            # Obtenir les recommandations
            recommendations = self.tax_analyzer._generate_recommendations(tax_analysis)
            
            return {
                "tax_analysis": tax_analysis,
                "obligations": obligations,
                "recommendations": recommendations,
                "quarter": self.current_quarter,
                "year": self.quarter_dates["year"]
            }
            
        except Exception as e:
            return {"error": str(e)}
            
    def _check_quarterly_compliance(self) -> Dict[str, Any]:
        """Vérifier la conformité trimestrielle"""
        try:
            # Vérifier les échéances
            upcoming_deadlines = fiscal_calendar.get_upcoming_deadlines(90)
            quarterly_deadlines = [d for d in upcoming_deadlines if d.type == "quarterly"]
            
            # Vérifier les risques de conformité
            compliance_risks = self.compliance_monitor._check_compliance_risks()
            
            # Vérifier les violations
            violations = self.compliance_monitor._check_violations()
            
            # Générer les alertes
            alerts = self.compliance_monitor._generate_alerts()
            
            return {
                "quarterly_deadlines": [d.name for d in quarterly_deadlines],
                "compliance_risks": compliance_risks,
                "violations": violations,
                "alerts": alerts,
                "compliance_score": self.compliance_monitor.get_compliance_score()
            }
            
        except Exception as e:
            return {"error": str(e)}
            
    def _prepare_quarterly_documents(self) -> Dict[str, Any]:
        """Préparer les documents fiscaux trimestriels"""
        try:
            # Générer les formulaires TPS/TVH
            gst_qst_forms = self.document_processor.generate_tax_forms(
                form_type="gst_qst_quarterly",
                period=f"Q{self.current_quarter} {self.quarter_dates['year']}"
            )
            
            # Préparer la documentation
            documentation = self.document_processor.create_documentation_package(
                package_type="quarterly",
                period=f"Q{self.current_quarter} {self.quarter_dates['year']}"
            )
            
            # Valider les formulaires
            validation_results = self.document_processor.validate_forms(gst_qst_forms)
            
            return {
                "forms_generated": len(gst_qst_forms),
                "documentation_package": documentation,
                "validation_results": validation_results,
                "quarter": self.current_quarter,
                "year": self.quarter_dates["year"]
            }
            
        except Exception as e:
            return {"error": str(e)}
            
    def _generate_quarterly_report(self) -> Dict[str, Any]:
        """Générer le rapport trimestriel complet"""
        try:
            # Générer le rapport complet
            comprehensive_report = self.reporting_specialist.generate_comprehensive_report(
                report_type="quarterly",
                period=f"Q{self.current_quarter} {self.quarter_dates['year']}"
            )
            
            # Créer les données pour le tableau de bord
            dashboard_data = self.reporting_specialist.create_dashboard_data(
                data_type="quarterly"
            )
            
            return {
                "comprehensive_report": comprehensive_report,
                "dashboard_data": dashboard_data,
                "quarter": self.current_quarter,
                "year": self.quarter_dates["year"]
            }
            
        except Exception as e:
            return {"error": str(e)}
            
    def _create_workflow_summary(self, steps: Dict[str, Any]) -> Dict[str, Any]:
        """Créer un résumé du workflow"""
        summary = {
            "quarter": self.current_quarter,
            "year": self.quarter_dates["year"],
            "execution_status": "completed",
            "total_transactions_processed": 0,
            "total_tax_obligations": 0,
            "compliance_score": 0,
            "documents_generated": 0,
            "alerts_generated": 0
        }
        
        # Extraire les informations des étapes
        if "data_collection" in steps and "error" not in steps["data_collection"]:
            summary["total_transactions_processed"] = steps["data_collection"].get("total_transactions", 0)
            
        if "compliance_check" in steps and "error" not in steps["compliance_check"]:
            summary["compliance_score"] = steps["compliance_check"].get("compliance_score", 0)
            summary["alerts_generated"] = len(steps["compliance_check"].get("alerts", []))
            
        if "document_preparation" in steps and "error" not in steps["document_preparation"]:
            summary["documents_generated"] = steps["document_preparation"].get("forms_generated", 0)
            
        if "tax_analysis" in steps and "error" not in steps["tax_analysis"]:
            obligations = steps["tax_analysis"].get("obligations", {})
            summary["total_tax_obligations"] = sum(obligations.values()) if obligations else 0
            
        return summary
        
    def get_next_quarterly_deadline(self) -> Optional[Dict[str, Any]]:
        """Obtenir la prochaine échéance trimestrielle"""
        upcoming_deadlines = fiscal_calendar.get_upcoming_deadlines(90)
        quarterly_deadlines = [d for d in upcoming_deadlines if d.type == "quarterly"]
        
        if quarterly_deadlines:
            next_deadline = min(quarterly_deadlines, key=lambda x: x.date)
            return {
                "name": next_deadline.name,
                "date": next_deadline.date.isoformat(),
                "description": next_deadline.description,
                "days_until": (next_deadline.date - datetime.now()).days
            }
        
        return None
        
    def is_quarterly_deadline_approaching(self, days_ahead: int = 30) -> bool:
        """Vérifier si une échéance trimestrielle approche"""
        next_deadline = self.get_next_quarterly_deadline()
        if next_deadline:
            return next_deadline["days_until"] <= days_ahead
        return False 
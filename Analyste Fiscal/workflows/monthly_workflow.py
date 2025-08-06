"""
Workflow mensuel automatisé pour la gestion fiscale
"""
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from crewai import Task, Crew, Process
from config.settings import config
from config.fiscal_calendar import fiscal_calendar
from agents.data_collector import DataCollectorAgent
from agents.tax_analyzer import TaxAnalyzerAgent
from agents.compliance_monitor import ComplianceMonitorAgent
from agents.reporting_specialist import ReportingSpecialistAgent

class MonthlyWorkflow:
    """Workflow automatisé pour les opérations fiscales mensuelles"""
    
    def __init__(self):
        self.data_collector = DataCollectorAgent()
        self.tax_analyzer = TaxAnalyzerAgent()
        self.compliance_monitor = ComplianceMonitorAgent()
        self.reporting_specialist = ReportingSpecialistAgent()
        
        self.current_month = datetime.now().month
        self.current_year = datetime.now().year
        self.month_dates = self._get_month_dates()
        
    def _get_month_dates(self) -> Dict[str, datetime]:
        """Obtenir les dates de début et fin du mois actuel"""
        start_date = datetime(self.current_year, self.current_month, 1)
        
        if self.current_month == 12:
            end_date = datetime(self.current_year + 1, 1, 1) - timedelta(days=1)
        else:
            end_date = datetime(self.current_year, self.current_month + 1, 1) - timedelta(days=1)
            
        return {
            "start": start_date,
            "end": end_date,
            "month": self.current_month,
            "year": self.current_year
        }
        
    def execute_monthly_workflow(self, force_refresh: bool = False) -> Dict[str, Any]:
        """Exécuter le workflow mensuel complet"""
        
        print(f"🚀 Démarrage du workflow mensuel {self._get_month_name()} {self.current_year}")
        print("=" * 60)
        
        workflow_results = {
            "month": self.current_month,
            "year": self.current_year,
            "execution_time": datetime.now().isoformat(),
            "steps": {},
            "summary": {}
        }
        
        try:
            # Étape 1: Collecte de données mensuelles
            print("📊 Étape 1: Collecte de données financières mensuelles...")
            monthly_data_collection = self._collect_monthly_data(force_refresh)
            workflow_results["steps"]["monthly_data_collection"] = monthly_data_collection
            
            # Étape 2: Analyse fiscale mensuelle
            print("🧮 Étape 2: Analyse fiscale mensuelle...")
            monthly_tax_analysis = self._analyze_monthly_taxes()
            workflow_results["steps"]["monthly_tax_analysis"] = monthly_tax_analysis
            
            # Étape 3: Vérification de conformité mensuelle
            print("✅ Étape 3: Vérification de conformité mensuelle...")
            monthly_compliance_check = self._check_monthly_compliance()
            workflow_results["steps"]["monthly_compliance_check"] = monthly_compliance_check
            
            # Étape 4: Génération du rapport mensuel
            print("📈 Étape 4: Génération du rapport mensuel...")
            monthly_report = self._generate_monthly_report()
            workflow_results["steps"]["monthly_report"] = monthly_report
            
            # Résumé du workflow
            workflow_results["summary"] = self._create_monthly_workflow_summary(workflow_results["steps"])
            
            print("✅ Workflow mensuel terminé avec succès!")
            return workflow_results
            
        except Exception as e:
            print(f"❌ Erreur lors de l'exécution du workflow mensuel: {e}")
            workflow_results["error"] = str(e)
            return workflow_results
            
    def _get_month_name(self) -> str:
        """Obtenir le nom du mois actuel"""
        month_names = [
            "Janvier", "Février", "Mars", "Avril", "Mai", "Juin",
            "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"
        ]
        return month_names[self.current_month - 1]
        
    def _collect_monthly_data(self, force_refresh: bool) -> Dict[str, Any]:
        """Collecter les données du mois"""
        try:
            # Collecter toutes les données
            all_data = self.data_collector.collect_all_data(force_refresh)
            
            # Filtrer pour le mois actuel
            monthly_transactions = self.data_collector.get_transactions(
                start_date=self.month_dates["start"],
                end_date=self.month_dates["end"]
            )
            
            # Obtenir les répartitions mensuelles
            monthly_revenue_breakdown = self.data_collector.get_revenue_breakdown("monthly")
            monthly_expense_breakdown = self.data_collector.get_expense_breakdown("monthly")
            monthly_tax_relevant_data = self.data_collector.get_tax_relevant_data()
            
            # Détecter les anomalies mensuelles
            monthly_anomalies = self.data_collector.detect_anomalies()
            
            return {
                "total_transactions": len(monthly_transactions),
                "monthly_revenue_breakdown": monthly_revenue_breakdown,
                "monthly_expense_breakdown": monthly_expense_breakdown,
                "monthly_tax_relevant_data": monthly_tax_relevant_data,
                "monthly_anomalies": monthly_anomalies,
                "month": self.current_month,
                "year": self.current_year,
                "collection_time": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {"error": str(e)}
            
    def _analyze_monthly_taxes(self) -> Dict[str, Any]:
        """Analyser les obligations fiscales du mois"""
        try:
            # Obtenir les transactions du mois
            transactions = self.data_collector.get_transactions(
                start_date=self.month_dates["start"],
                end_date=self.month_dates["end"]
            )
            
            # Analyser les taxes mensuelles
            monthly_tax_analysis = self.tax_analyzer.analyze_transactions(transactions)
            
            # Calculer les obligations mensuelles
            monthly_obligations = self.tax_analyzer._determine_obligations(monthly_tax_analysis)
            
            # Obtenir les recommandations mensuelles
            monthly_recommendations = self.tax_analyzer._generate_recommendations(monthly_tax_analysis)
            
            # Calculer les prévisions fiscales mensuelles
            monthly_tax_forecast = self.tax_analyzer.get_tax_forecast(period="monthly")
            
            return {
                "monthly_tax_analysis": monthly_tax_analysis,
                "monthly_obligations": monthly_obligations,
                "monthly_recommendations": monthly_recommendations,
                "monthly_tax_forecast": monthly_tax_forecast,
                "month": self.current_month,
                "year": self.current_year
            }
            
        except Exception as e:
            return {"error": str(e)}
            
    def _check_monthly_compliance(self) -> Dict[str, Any]:
        """Vérifier la conformité mensuelle"""
        try:
            # Vérifier les échéances mensuelles
            monthly_deadlines = fiscal_calendar.get_deadlines_by_type("monthly", self.current_year)
            current_month_deadlines = [d for d in monthly_deadlines if d.date.month == self.current_month]
            
            # Vérifier les risques de conformité mensuels
            monthly_compliance_risks = self.compliance_monitor._check_compliance_risks()
            
            # Vérifier les violations mensuelles
            monthly_violations = self.compliance_monitor._check_violations()
            
            # Générer les alertes mensuelles
            monthly_alerts = self.compliance_monitor._generate_alerts()
            
            # Obtenir le score de conformité mensuel
            monthly_compliance_score = self.compliance_monitor.get_compliance_score()
            
            return {
                "monthly_deadlines": [d.name for d in current_month_deadlines],
                "monthly_compliance_risks": monthly_compliance_risks,
                "monthly_violations": monthly_violations,
                "monthly_alerts": monthly_alerts,
                "monthly_compliance_score": monthly_compliance_score,
                "month": self.current_month,
                "year": self.current_year
            }
            
        except Exception as e:
            return {"error": str(e)}
            
    def _generate_monthly_report(self) -> Dict[str, Any]:
        """Générer le rapport mensuel complet"""
        try:
            # Générer le rapport mensuel complet
            comprehensive_monthly_report = self.reporting_specialist.generate_comprehensive_report(
                report_type="monthly",
                period=f"{self._get_month_name()} {self.current_year}"
            )
            
            # Créer les données pour le tableau de bord mensuel
            monthly_dashboard_data = self.reporting_specialist.create_dashboard_data(
                data_type="monthly"
            )
            
            # Générer l'historique des rapports mensuels
            monthly_report_history = self.reporting_specialist.get_report_history()
            
            # Exporter le rapport mensuel
            monthly_export_results = self.reporting_specialist.export_report(
                report_type="monthly",
                format="comprehensive"
            )
            
            return {
                "comprehensive_monthly_report": comprehensive_monthly_report,
                "monthly_dashboard_data": monthly_dashboard_data,
                "monthly_report_history": monthly_report_history,
                "monthly_export_results": monthly_export_results,
                "month": self.current_month,
                "year": self.current_year
            }
            
        except Exception as e:
            return {"error": str(e)}
            
    def _create_monthly_workflow_summary(self, steps: Dict[str, Any]) -> Dict[str, Any]:
        """Créer un résumé du workflow mensuel"""
        summary = {
            "month": self.current_month,
            "year": self.current_year,
            "execution_status": "completed",
            "total_transactions_processed": 0,
            "total_monthly_tax_obligations": 0,
            "monthly_compliance_score": 0,
            "monthly_alerts_generated": 0
        }
        
        # Extraire les informations des étapes
        if "monthly_data_collection" in steps and "error" not in steps["monthly_data_collection"]:
            summary["total_transactions_processed"] = steps["monthly_data_collection"].get("total_transactions", 0)
            
        if "monthly_compliance_check" in steps and "error" not in steps["monthly_compliance_check"]:
            summary["monthly_compliance_score"] = steps["monthly_compliance_check"].get("monthly_compliance_score", 0)
            summary["monthly_alerts_generated"] = len(steps["monthly_compliance_check"].get("monthly_alerts", []))
            
        if "monthly_tax_analysis" in steps and "error" not in steps["monthly_tax_analysis"]:
            obligations = steps["monthly_tax_analysis"].get("monthly_obligations", {})
            summary["total_monthly_tax_obligations"] = sum(obligations.values()) if obligations else 0
            
        return summary
        
    def get_next_monthly_deadline(self) -> Optional[Dict[str, Any]]:
        """Obtenir la prochaine échéance mensuelle"""
        monthly_deadlines = fiscal_calendar.get_deadlines_by_type("monthly", self.current_year)
        upcoming_monthly_deadlines = [d for d in monthly_deadlines if d.date > datetime.now()]
        
        if upcoming_monthly_deadlines:
            next_deadline = min(upcoming_monthly_deadlines, key=lambda x: x.date)
            return {
                "name": next_deadline.name,
                "date": next_deadline.date.isoformat(),
                "description": next_deadline.description,
                "days_until": (next_deadline.date - datetime.now()).days
            }
        
        return None
        
    def is_monthly_deadline_approaching(self, days_ahead: int = 15) -> bool:
        """Vérifier si une échéance mensuelle approche"""
        next_deadline = self.get_next_monthly_deadline()
        if next_deadline:
            return next_deadline["days_until"] <= days_ahead
        return False
        
    def get_monthly_summary(self) -> Dict[str, Any]:
        """Obtenir un résumé du mois"""
        return {
            "month": self.current_month,
            "year": self.current_year,
            "month_name": self._get_month_name(),
            "month_period": {
                "start": self.month_dates["start"].isoformat(),
                "end": self.month_dates["end"].isoformat()
            },
            "next_monthly_deadline": self.get_next_monthly_deadline(),
            "monthly_deadlines_approaching": self.is_monthly_deadline_approaching()
        } 
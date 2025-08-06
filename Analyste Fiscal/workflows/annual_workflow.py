"""
Workflow annuel automatisé pour la gestion fiscale
"""
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from crewai import Task, Crew, Process
from config.settings import config
from config.fiscal_calendar import fiscal_calendar
from agents.data_collector import DataCollectorAgent
from agents.tax_analyzer import TaxAnalyzerAgent
from agents.compliance_monitor import ComplianceMonitorAgent
from agents.strategic_advisor import StrategicAdvisorAgent
from agents.document_processor import DocumentProcessorAgent
from agents.reporting_specialist import ReportingSpecialistAgent

class AnnualWorkflow:
    """Workflow automatisé pour les opérations fiscales annuelles"""
    
    def __init__(self):
        self.data_collector = DataCollectorAgent()
        self.tax_analyzer = TaxAnalyzerAgent()
        self.compliance_monitor = ComplianceMonitorAgent()
        self.strategic_advisor = StrategicAdvisorAgent()
        self.document_processor = DocumentProcessorAgent()
        self.reporting_specialist = ReportingSpecialistAgent()
        
        self.current_year = datetime.now().year
        self.fiscal_period = config.get_fiscal_period()
        
    def execute_annual_workflow(self, force_refresh: bool = False) -> Dict[str, Any]:
        """Exécuter le workflow annuel complet"""
        
        print(f"🚀 Démarrage du workflow annuel {self.current_year}")
        print("=" * 60)
        
        workflow_results = {
            "year": self.current_year,
            "execution_time": datetime.now().isoformat(),
            "steps": {},
            "summary": {}
        }
        
        try:
            # Étape 1: Collecte de données annuelles
            print("📊 Étape 1: Collecte de données financières annuelles...")
            annual_data_collection = self._collect_annual_data(force_refresh)
            workflow_results["steps"]["annual_data_collection"] = annual_data_collection
            
            # Étape 2: Analyse fiscale annuelle complète
            print("🧮 Étape 2: Analyse fiscale annuelle complète...")
            annual_tax_analysis = self._analyze_annual_taxes()
            workflow_results["steps"]["annual_tax_analysis"] = annual_tax_analysis
            
            # Étape 3: Planification stratégique
            print("🎯 Étape 3: Planification stratégique pour l'année suivante...")
            strategic_planning = self._perform_strategic_planning()
            workflow_results["steps"]["strategic_planning"] = strategic_planning
            
            # Étape 4: Vérification de conformité annuelle
            print("✅ Étape 4: Vérification de conformité annuelle...")
            annual_compliance_check = self._check_annual_compliance()
            workflow_results["steps"]["annual_compliance_check"] = annual_compliance_check
            
            # Étape 5: Préparation des déclarations annuelles
            print("📄 Étape 5: Préparation des déclarations annuelles...")
            annual_document_preparation = self._prepare_annual_documents()
            workflow_results["steps"]["annual_document_preparation"] = annual_document_preparation
            
            # Étape 6: Génération du rapport annuel
            print("📈 Étape 6: Génération du rapport annuel complet...")
            annual_report = self._generate_annual_report()
            workflow_results["steps"]["annual_report"] = annual_report
            
            # Résumé du workflow
            workflow_results["summary"] = self._create_annual_workflow_summary(workflow_results["steps"])
            
            print("✅ Workflow annuel terminé avec succès!")
            return workflow_results
            
        except Exception as e:
            print(f"❌ Erreur lors de l'exécution du workflow annuel: {e}")
            workflow_results["error"] = str(e)
            return workflow_results
            
    def _collect_annual_data(self, force_refresh: bool) -> Dict[str, Any]:
        """Collecter les données de l'année fiscale"""
        try:
            # Collecter toutes les données
            all_data = self.data_collector.collect_all_data(force_refresh)
            
            # Filtrer pour l'année fiscale
            annual_transactions = self.data_collector.get_transactions(
                start_date=self.fiscal_period["start"],
                end_date=self.fiscal_period["end"]
            )
            
            # Obtenir les répartitions annuelles
            annual_revenue_breakdown = self.data_collector.get_revenue_breakdown("annual")
            annual_expense_breakdown = self.data_collector.get_expense_breakdown("annual")
            annual_tax_relevant_data = self.data_collector.get_tax_relevant_data()
            
            # Détecter les anomalies annuelles
            annual_anomalies = self.data_collector.detect_anomalies()
            
            return {
                "total_transactions": len(annual_transactions),
                "annual_revenue_breakdown": annual_revenue_breakdown,
                "annual_expense_breakdown": annual_expense_breakdown,
                "annual_tax_relevant_data": annual_tax_relevant_data,
                "annual_anomalies": annual_anomalies,
                "fiscal_period": {
                    "start": self.fiscal_period["start"].isoformat(),
                    "end": self.fiscal_period["end"].isoformat(),
                    "year": self.fiscal_period["year"]
                },
                "collection_time": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {"error": str(e)}
            
    def _analyze_annual_taxes(self) -> Dict[str, Any]:
        """Analyser les obligations fiscales annuelles"""
        try:
            # Obtenir les transactions de l'année
            transactions = self.data_collector.get_transactions(
                start_date=self.fiscal_period["start"],
                end_date=self.fiscal_period["end"]
            )
            
            # Analyser les taxes annuelles
            annual_tax_analysis = self.tax_analyzer.analyze_transactions(transactions)
            
            # Calculer les obligations annuelles
            annual_obligations = self.tax_analyzer._determine_obligations(annual_tax_analysis)
            
            # Obtenir les recommandations annuelles
            annual_recommendations = self.tax_analyzer._generate_recommendations(annual_tax_analysis)
            
            # Calculer les prévisions fiscales
            tax_forecast = self.tax_analyzer.get_tax_forecast(period="annual")
            
            # Analyser l'efficacité fiscale
            tax_efficiency = self.tax_analyzer.analyze_tax_efficiency()
            
            return {
                "annual_tax_analysis": annual_tax_analysis,
                "annual_obligations": annual_obligations,
                "annual_recommendations": annual_recommendations,
                "tax_forecast": tax_forecast,
                "tax_efficiency": tax_efficiency,
                "fiscal_year": self.current_year
            }
            
        except Exception as e:
            return {"error": str(e)}
            
    def _perform_strategic_planning(self) -> Dict[str, Any]:
        """Effectuer la planification stratégique pour l'année suivante"""
        try:
            # Analyser les opportunités d'optimisation
            optimization_opportunities = self.strategic_advisor.analyze_tax_optimization_opportunities()
            
            # Créer un plan stratégique
            strategic_plan = self.strategic_advisor._create_implementation_plan(
                opportunities=optimization_opportunities
            )
            
            # Analyser le ROI des stratégies
            roi_analysis = self.strategic_advisor._analyze_roi(strategic_plan)
            
            # Obtenir les comparaisons de benchmark
            benchmark_comparison = self.strategic_advisor.get_benchmark_comparison()
            
            return {
                "optimization_opportunities": optimization_opportunities,
                "strategic_plan": strategic_plan,
                "roi_analysis": roi_analysis,
                "benchmark_comparison": benchmark_comparison,
                "planning_year": self.current_year + 1
            }
            
        except Exception as e:
            return {"error": str(e)}
            
    def _check_annual_compliance(self) -> Dict[str, Any]:
        """Vérifier la conformité annuelle"""
        try:
            # Vérifier les échéances annuelles
            annual_deadlines = fiscal_calendar.get_deadlines_by_type("annual", self.current_year)
            upcoming_annual_deadlines = [d for d in annual_deadlines if d.date > datetime.now()]
            
            # Vérifier les risques de conformité annuels
            annual_compliance_risks = self.compliance_monitor._check_compliance_risks()
            
            # Vérifier les violations annuelles
            annual_violations = self.compliance_monitor._check_violations()
            
            # Préparer la documentation d'audit
            audit_documentation = self.compliance_monitor.prepare_audit_documentation()
            
            # Obtenir le score de conformité annuel
            annual_compliance_score = self.compliance_monitor.get_compliance_score()
            
            return {
                "annual_deadlines": [d.name for d in upcoming_annual_deadlines],
                "annual_compliance_risks": annual_compliance_risks,
                "annual_violations": annual_violations,
                "audit_documentation": audit_documentation,
                "annual_compliance_score": annual_compliance_score
            }
            
        except Exception as e:
            return {"error": str(e)}
            
    def _prepare_annual_documents(self) -> Dict[str, Any]:
        """Préparer les documents fiscaux annuels"""
        try:
            # Générer les formulaires T1 (fédéral)
            t1_forms = self.document_processor.generate_tax_forms(
                form_type="t1_annual",
                period=f"{self.current_year}"
            )
            
            # Générer les formulaires TP-1 (Québec)
            tp1_forms = self.document_processor.generate_tax_forms(
                form_type="tp1_annual",
                period=f"{self.current_year}"
            )
            
            # Générer les formulaires T2 (si applicable)
            t2_forms = self.document_processor.generate_tax_forms(
                form_type="t2_annual",
                period=f"{self.current_year}"
            )
            
            # Préparer la documentation annuelle
            annual_documentation = self.document_processor.create_documentation_package(
                package_type="annual",
                period=f"{self.current_year}"
            )
            
            # Valider tous les formulaires
            all_forms = t1_forms + tp1_forms + t2_forms
            validation_results = self.document_processor.validate_forms(all_forms)
            
            return {
                "t1_forms_generated": len(t1_forms),
                "tp1_forms_generated": len(tp1_forms),
                "t2_forms_generated": len(t2_forms),
                "total_forms_generated": len(all_forms),
                "annual_documentation": annual_documentation,
                "validation_results": validation_results,
                "fiscal_year": self.current_year
            }
            
        except Exception as e:
            return {"error": str(e)}
            
    def _generate_annual_report(self) -> Dict[str, Any]:
        """Générer le rapport annuel complet"""
        try:
            # Générer le rapport annuel complet
            comprehensive_annual_report = self.reporting_specialist.generate_comprehensive_report(
                report_type="annual",
                period=f"{self.current_year}"
            )
            
            # Créer les données pour le tableau de bord annuel
            annual_dashboard_data = self.reporting_specialist.create_dashboard_data(
                data_type="annual"
            )
            
            # Générer l'historique des rapports
            report_history = self.reporting_specialist.get_report_history()
            
            # Exporter le rapport
            export_results = self.reporting_specialist.export_report(
                report_type="annual",
                format="comprehensive"
            )
            
            return {
                "comprehensive_annual_report": comprehensive_annual_report,
                "annual_dashboard_data": annual_dashboard_data,
                "report_history": report_history,
                "export_results": export_results,
                "fiscal_year": self.current_year
            }
            
        except Exception as e:
            return {"error": str(e)}
            
    def _create_annual_workflow_summary(self, steps: Dict[str, Any]) -> Dict[str, Any]:
        """Créer un résumé du workflow annuel"""
        summary = {
            "year": self.current_year,
            "execution_status": "completed",
            "total_transactions_processed": 0,
            "total_annual_tax_obligations": 0,
            "annual_compliance_score": 0,
            "annual_documents_generated": 0,
            "strategic_opportunities_identified": 0,
            "annual_alerts_generated": 0
        }
        
        # Extraire les informations des étapes
        if "annual_data_collection" in steps and "error" not in steps["annual_data_collection"]:
            summary["total_transactions_processed"] = steps["annual_data_collection"].get("total_transactions", 0)
            
        if "annual_compliance_check" in steps and "error" not in steps["annual_compliance_check"]:
            summary["annual_compliance_score"] = steps["annual_compliance_check"].get("annual_compliance_score", 0)
            
        if "annual_document_preparation" in steps and "error" not in steps["annual_document_preparation"]:
            summary["annual_documents_generated"] = steps["annual_document_preparation"].get("total_forms_generated", 0)
            
        if "strategic_planning" in steps and "error" not in steps["strategic_planning"]:
            opportunities = steps["strategic_planning"].get("optimization_opportunities", {})
            summary["strategic_opportunities_identified"] = len(opportunities.get("opportunities", []))
            
        if "annual_tax_analysis" in steps and "error" not in steps["annual_tax_analysis"]:
            obligations = steps["annual_tax_analysis"].get("annual_obligations", {})
            summary["total_annual_tax_obligations"] = sum(obligations.values()) if obligations else 0
            
        return summary
        
    def get_next_annual_deadline(self) -> Optional[Dict[str, Any]]:
        """Obtenir la prochaine échéance annuelle"""
        annual_deadlines = fiscal_calendar.get_deadlines_by_type("annual", self.current_year)
        upcoming_annual_deadlines = [d for d in annual_deadlines if d.date > datetime.now()]
        
        if upcoming_annual_deadlines:
            next_deadline = min(upcoming_annual_deadlines, key=lambda x: x.date)
            return {
                "name": next_deadline.name,
                "date": next_deadline.date.isoformat(),
                "description": next_deadline.description,
                "days_until": (next_deadline.date - datetime.now()).days
            }
        
        return None
        
    def is_annual_deadline_approaching(self, days_ahead: int = 60) -> bool:
        """Vérifier si une échéance annuelle approche"""
        next_deadline = self.get_next_annual_deadline()
        if next_deadline:
            return next_deadline["days_until"] <= days_ahead
        return False
        
    def get_fiscal_year_summary(self) -> Dict[str, Any]:
        """Obtenir un résumé de l'année fiscale"""
        return {
            "fiscal_year": self.current_year,
            "fiscal_period": {
                "start": self.fiscal_period["start"].isoformat(),
                "end": self.fiscal_period["end"].isoformat()
            },
            "next_annual_deadline": self.get_next_annual_deadline(),
            "annual_deadlines_approaching": self.is_annual_deadline_approaching()
        } 
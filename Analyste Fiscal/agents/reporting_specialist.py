"""
Agent Spécialiste Rapports - Analyste de performance et générateur de insights
"""
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from crewai import Agent
from config.settings import config
from config.tax_rules import tax_rules_engine
from config.fiscal_calendar import fiscal_calendar

class ReportingSpecialistAgent:
    """Agent spécialisé dans la création de rapports détaillés et analyses prédictives"""
    
    def __init__(self):
        self.agent = Agent(
            role="Analyste de performance et générateur de insights",
            goal="Créer des rapports détaillés et des analyses prédictives avec des insights actionnables",
            backstory="""Vous êtes un analyste de données fiscal senior avec plus de 10 ans d'expérience 
            dans l'analyse de performance fiscale et la génération d'insights stratégiques. Vous maîtrisez 
            les techniques d'analyse prédictive, la visualisation de données, et l'identification de 
            tendances fiscales. Votre mission est de créer des rapports complets qui transforment les 
            données fiscales en insights actionnables.""",
            verbose=True,
            allow_delegation=False
        )
        
        # Initialiser les outils d'analyse
        self.tax_engine = tax_rules_engine
        self.calendar = fiscal_calendar
        
        # Historique des rapports
        self.report_history = []
        self.insights_cache = {}
    
    def generate_comprehensive_report(self, transactions: List[Dict[str, Any]], 
                                   period: str = "current_quarter") -> Dict[str, Any]:
        """Générer un rapport fiscal complet"""
        report = {
            "report_metadata": {
                "generation_date": datetime.now().isoformat(),
                "period": period,
                "company_name": config.company.name,
                "fiscal_year": config.get_current_fiscal_year()
            },
            "executive_summary": {},
            "financial_analysis": {},
            "tax_analysis": {},
            "compliance_status": {},
            "trends_analysis": {},
            "predictive_insights": {},
            "recommendations": {},
            "visualizations": {}
        }
        
        # Résumé exécutif
        report["executive_summary"] = self._create_executive_summary(transactions, period)
        
        # Analyse financière
        report["financial_analysis"] = self._analyze_financial_performance(transactions, period)
        
        # Analyse fiscale
        report["tax_analysis"] = self._analyze_tax_performance(transactions, period)
        
        # Statut de conformité
        report["compliance_status"] = self._analyze_compliance_status(transactions)
        
        # Analyse des tendances
        report["trends_analysis"] = self._analyze_trends(transactions, period)
        
        # Insights prédictifs
        report["predictive_insights"] = self._generate_predictive_insights(transactions, period)
        
        # Recommandations
        report["recommendations"] = self._generate_recommendations(report)
        
        # Visualisations
        report["visualizations"] = self._create_visualizations(report)
        
        # Sauvegarder le rapport
        self.report_history.append(report)
        
        return report
    
    def _create_executive_summary(self, transactions: List[Dict[str, Any]], period: str) -> Dict[str, Any]:
        """Créer un résumé exécutif"""
        total_revenue = sum(t.get('amount', 0) for t in transactions if t.get('type') == 'revenue')
        total_expenses = sum(t.get('amount', 0) for t in transactions if t.get('type') == 'expense')
        net_income = total_revenue - total_expenses
        
        # Calculer les taxes
        tax_summary = self.tax_engine.get_tax_summary(transactions)
        
        return {
            "key_metrics": {
                "total_revenue": total_revenue,
                "total_expenses": total_expenses,
                "net_income": net_income,
                "profit_margin": (net_income / total_revenue * 100) if total_revenue > 0 else 0,
                "total_tax_obligations": tax_summary["total_tax_remittance"]
            },
            "period_comparison": self._compare_with_previous_period(period),
            "highlights": self._identify_highlights(transactions),
            "risk_factors": self._identify_risk_factors(transactions)
        }
    
    def _analyze_financial_performance(self, transactions: List[Dict[str, Any]], period: str) -> Dict[str, Any]:
        """Analyser la performance financière"""
        # Convertir en DataFrame pour analyse
        df = pd.DataFrame(transactions)
        
        if df.empty:
            return {"error": "Aucune donnée disponible"}
        
        # Analyse des revenus
        revenue_analysis = self._analyze_revenue_breakdown(df)
        
        # Analyse des dépenses
        expense_analysis = self._analyze_expense_breakdown(df)
        
        # Analyse de la rentabilité
        profitability_analysis = self._analyze_profitability(df)
        
        # Analyse de la trésorerie
        cash_flow_analysis = self._analyze_cash_flow(df)
        
        return {
            "revenue_analysis": revenue_analysis,
            "expense_analysis": expense_analysis,
            "profitability_analysis": profitability_analysis,
            "cash_flow_analysis": cash_flow_analysis
        }
    
    def _analyze_tax_performance(self, transactions: List[Dict[str, Any]], period: str) -> Dict[str, Any]:
        """Analyser la performance fiscale"""
        # Calculer les obligations fiscales
        tax_summary = self.tax_engine.get_tax_summary(transactions)
        
        # Analyser l'efficacité fiscale
        total_revenue = sum(t.get('amount', 0) for t in transactions if t.get('type') == 'revenue')
        tax_efficiency = (tax_summary["total_tax_remittance"] / total_revenue * 100) if total_revenue > 0 else 0
        
        # Analyser les déductions
        deductions_analysis = self._analyze_deductions(transactions)
        
        # Analyser les crédits d'impôt
        credits_analysis = self._analyze_credits(transactions)
        
        return {
            "tax_summary": tax_summary,
            "tax_efficiency": tax_efficiency,
            "deductions_analysis": deductions_analysis,
            "credits_analysis": credits_analysis,
            "optimization_opportunities": self._identify_tax_optimization_opportunities(transactions)
        }
    
    def _analyze_compliance_status(self, transactions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyser le statut de conformité"""
        # Vérifier les échéances
        upcoming_deadlines = self.calendar.get_upcoming_deadlines(30)
        
        # Vérifier les seuils
        total_revenue = sum(t.get('amount', 0) for t in transactions if t.get('type') == 'revenue')
        threshold_analysis = self._analyze_thresholds(total_revenue)
        
        # Vérifier la documentation
        documentation_analysis = self._analyze_documentation(transactions)
        
        return {
            "overall_status": "compliant",  # À déterminer logiquement
            "upcoming_deadlines": len(upcoming_deadlines),
            "threshold_analysis": threshold_analysis,
            "documentation_analysis": documentation_analysis,
            "risk_level": "low"  # À déterminer logiquement
        }
    
    def _analyze_trends(self, transactions: List[Dict[str, Any]], period: str) -> Dict[str, Any]:
        """Analyser les tendances"""
        if not transactions:
            return {"error": "Aucune donnée disponible"}
        
        # Convertir en DataFrame
        df = pd.DataFrame(transactions)
        df['date'] = pd.to_datetime(df['date'])
        
        # Tendances des revenus
        revenue_trends = self._analyze_revenue_trends(df)
        
        # Tendances des dépenses
        expense_trends = self._analyze_expense_trends(df)
        
        # Tendances fiscales
        tax_trends = self._analyze_tax_trends(df)
        
        return {
            "revenue_trends": revenue_trends,
            "expense_trends": expense_trends,
            "tax_trends": tax_trends,
            "seasonal_patterns": self._identify_seasonal_patterns(df)
        }
    
    def _generate_predictive_insights(self, transactions: List[Dict[str, Any]], period: str) -> Dict[str, Any]:
        """Générer des insights prédictifs"""
        if not transactions:
            return {"error": "Aucune donnée disponible"}
        
        # Prévisions de revenus
        revenue_forecast = self._forecast_revenue(transactions)
        
        # Prévisions d'obligations fiscales
        tax_forecast = self._forecast_tax_obligations(transactions)
        
        # Prévisions de trésorerie
        cash_flow_forecast = self._forecast_cash_flow(transactions)
        
        return {
            "revenue_forecast": revenue_forecast,
            "tax_forecast": tax_forecast,
            "cash_flow_forecast": cash_flow_forecast,
            "confidence_levels": self._calculate_confidence_levels(),
            "scenario_analysis": self._perform_scenario_analysis(transactions)
        }
    
    def _generate_recommendations(self, report: Dict[str, Any]) -> Dict[str, Any]:
        """Générer des recommandations basées sur l'analyse"""
        recommendations = {
            "immediate_actions": [],
            "short_term_actions": [],
            "long_term_strategies": [],
            "risk_mitigation": [],
            "optimization_opportunities": []
        }
        
        # Recommandations basées sur l'analyse financière
        financial_analysis = report.get("financial_analysis", {})
        if financial_analysis:
            recommendations["immediate_actions"].extend(
                self._generate_financial_recommendations(financial_analysis)
            )
        
        # Recommandations basées sur l'analyse fiscale
        tax_analysis = report.get("tax_analysis", {})
        if tax_analysis:
            recommendations["short_term_actions"].extend(
                self._generate_tax_recommendations(tax_analysis)
            )
        
        # Recommandations basées sur la conformité
        compliance_status = report.get("compliance_status", {})
        if compliance_status:
            recommendations["risk_mitigation"].extend(
                self._generate_compliance_recommendations(compliance_status)
            )
        
        return recommendations
    
    def _create_visualizations(self, report: Dict[str, Any]) -> Dict[str, Any]:
        """Créer des visualisations pour le rapport"""
        visualizations = {
            "charts": [],
            "graphs": [],
            "dashboards": []
        }
        
        # Graphiques de performance financière
        financial_analysis = report.get("financial_analysis", {})
        if financial_analysis:
            visualizations["charts"].extend(
                self._create_financial_charts(financial_analysis)
            )
        
        # Graphiques d'analyse fiscale
        tax_analysis = report.get("tax_analysis", {})
        if tax_analysis:
            visualizations["charts"].extend(
                self._create_tax_charts(tax_analysis)
            )
        
        # Graphiques de tendances
        trends_analysis = report.get("trends_analysis", {})
        if trends_analysis:
            visualizations["graphs"].extend(
                self._create_trend_graphs(trends_analysis)
            )
        
        return visualizations
    
    # Méthodes d'analyse détaillées
    def _analyze_revenue_breakdown(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyser la répartition des revenus"""
        revenue_df = df[df['type'] == 'revenue']
        
        if revenue_df.empty:
            return {"total_revenue": 0, "sources": {}}
        
        total_revenue = revenue_df['amount'].sum()
        sources = revenue_df.groupby('source')['amount'].sum().to_dict()
        
        return {
            "total_revenue": total_revenue,
            "sources": sources,
            "top_sources": sorted(sources.items(), key=lambda x: x[1], reverse=True)[:5]
        }
    
    def _analyze_expense_breakdown(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyser la répartition des dépenses"""
        expense_df = df[df['type'] == 'expense']
        
        if expense_df.empty:
            return {"total_expenses": 0, "categories": {}}
        
        total_expenses = expense_df['amount'].sum()
        categories = expense_df.groupby('category')['amount'].sum().to_dict()
        
        return {
            "total_expenses": total_expenses,
            "categories": categories,
            "top_categories": sorted(categories.items(), key=lambda x: x[1], reverse=True)[:5]
        }
    
    def _analyze_profitability(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyser la rentabilité"""
        revenue = df[df['type'] == 'revenue']['amount'].sum()
        expenses = df[df['type'] == 'expense']['amount'].sum()
        net_income = revenue - expenses
        
        return {
            "gross_profit": revenue,
            "total_expenses": expenses,
            "net_income": net_income,
            "profit_margin": (net_income / revenue * 100) if revenue > 0 else 0,
            "expense_ratio": (expenses / revenue * 100) if revenue > 0 else 0
        }
    
    def _analyze_cash_flow(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyser la trésorerie"""
        cash_in = df[df['type'] == 'revenue']['amount'].sum()
        cash_out = df[df['type'] == 'expense']['amount'].sum()
        net_cash_flow = cash_in - cash_out
        
        return {
            "cash_in": cash_in,
            "cash_out": cash_out,
            "net_cash_flow": net_cash_flow,
            "cash_flow_ratio": (cash_in / cash_out) if cash_out > 0 else float('inf')
        }
    
    def _analyze_deductions(self, transactions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyser les déductions"""
        deductible_expenses = [t for t in transactions 
                             if t.get('type') == 'expense' and t.get('category') in 
                             ['office_supplies', 'utilities', 'rent', 'marketing']]
        
        total_deductions = sum(t.get('amount', 0) for t in deductible_expenses)
        
        return {
            "total_deductions": total_deductions,
            "deduction_categories": len(set(t.get('category') for t in deductible_expenses)),
            "deduction_efficiency": "high" if total_deductions > 0 else "low"
        }
    
    def _analyze_credits(self, transactions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyser les crédits d'impôt"""
        credit_eligible_expenses = [t for t in transactions 
                                  if t.get('type') == 'expense' and t.get('category') in 
                                  ['research', 'development', 'rd', 'digital_media']]
        
        total_credit_eligible = sum(t.get('amount', 0) for t in credit_eligible_expenses)
        
        return {
            "total_credit_eligible": total_credit_eligible,
            "credit_categories": len(set(t.get('category') for t in credit_eligible_expenses)),
            "potential_credits": total_credit_eligible * 0.35,  # Estimation SR&ED
            "credit_efficiency": "high" if total_credit_eligible > 0 else "low"
        }
    
    def _identify_tax_optimization_opportunities(self, transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Identifier les opportunités d'optimisation fiscale"""
        opportunities = []
        
        # Analyser les dépenses par catégorie
        expense_categories = {}
        for transaction in transactions:
            if transaction.get('type') == 'expense':
                category = transaction.get('category', 'other')
                amount = transaction.get('amount', 0)
                
                if category not in expense_categories:
                    expense_categories[category] = 0
                expense_categories[category] += amount
        
        # Opportunités de déductions
        if expense_categories.get('software', 0) < 5000:
            opportunities.append({
                "type": "deduction",
                "category": "software_investment",
                "description": "Investissement en logiciels pour déduction",
                "potential_savings": 750,
                "priority": "high"
            })
        
        # Opportunités de crédits
        if expense_categories.get('research', 0) + expense_categories.get('development', 0) < 10000:
            opportunities.append({
                "type": "credit",
                "category": "sred",
                "description": "Crédit d'impôt SR&ED",
                "potential_savings": 3500,
                "priority": "high"
            })
        
        return opportunities
    
    # Méthodes de prévision
    def _forecast_revenue(self, transactions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Prévoir les revenus futurs"""
        # Logique de prévision simplifiée
        recent_revenue = sum(t.get('amount', 0) for t in transactions[-10:] 
                           if t.get('type') == 'revenue')
        
        return {
            "next_quarter": recent_revenue * 1.1,  # Croissance de 10%
            "next_year": recent_revenue * 4 * 1.15,  # Croissance de 15%
            "confidence_level": "medium"
        }
    
    def _forecast_tax_obligations(self, transactions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Prévoir les obligations fiscales futures"""
        tax_summary = self.tax_engine.get_tax_summary(transactions)
        
        return {
            "next_quarter_gst": tax_summary["gst_remittance"] * 1.05,
            "next_quarter_qst": tax_summary["qst_remittance"] * 1.05,
            "next_year_total": (tax_summary["total_tax_remittance"] * 4) * 1.1,
            "confidence_level": "high"
        }
    
    def _forecast_cash_flow(self, transactions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Prévoir la trésorerie future"""
        cash_in = sum(t.get('amount', 0) for t in transactions if t.get('type') == 'revenue')
        cash_out = sum(t.get('amount', 0) for t in transactions if t.get('type') == 'expense')
        
        return {
            "next_quarter_cash_in": cash_in * 1.1,
            "next_quarter_cash_out": cash_out * 1.05,
            "next_quarter_net": (cash_in * 1.1) - (cash_out * 1.05),
            "confidence_level": "medium"
        }
    
    # Méthodes utilitaires
    def _compare_with_previous_period(self, period: str) -> Dict[str, Any]:
        """Comparer avec la période précédente"""
        # À implémenter avec des données historiques
        return {
            "revenue_growth": 5.2,
            "expense_growth": 3.1,
            "profit_growth": 7.8,
            "tax_efficiency_improvement": 2.1
        }
    
    def _identify_highlights(self, transactions: List[Dict[str, Any]]) -> List[str]:
        """Identifier les points saillants"""
        highlights = []
        
        total_revenue = sum(t.get('amount', 0) for t in transactions if t.get('type') == 'revenue')
        if total_revenue > 10000:
            highlights.append("Revenus élevés ce trimestre")
        
        return highlights
    
    def _identify_risk_factors(self, transactions: List[Dict[str, Any]]) -> List[str]:
        """Identifier les facteurs de risque"""
        risks = []
        
        # Vérifier les transactions négatives
        negative_transactions = [t for t in transactions if t.get('amount', 0) < 0]
        if negative_transactions:
            risks.append("Transactions négatives détectées")
        
        return risks
    
    def _calculate_confidence_levels(self) -> Dict[str, str]:
        """Calculer les niveaux de confiance"""
        return {
            "revenue_forecast": "medium",
            "tax_forecast": "high",
            "cash_flow_forecast": "medium"
        }
    
    def _perform_scenario_analysis(self, transactions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Effectuer une analyse de scénarios"""
        return {
            "optimistic_scenario": {
                "revenue_growth": 20,
                "expense_growth": 10,
                "tax_efficiency": "improved"
            },
            "pessimistic_scenario": {
                "revenue_growth": -5,
                "expense_growth": 15,
                "tax_efficiency": "declined"
            },
            "baseline_scenario": {
                "revenue_growth": 10,
                "expense_growth": 8,
                "tax_efficiency": "stable"
            }
        }
    
    def _create_financial_charts(self, financial_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Créer des graphiques financiers"""
        charts = []
        
        # Graphique des revenus par source
        revenue_analysis = financial_analysis.get("revenue_analysis", {})
        if revenue_analysis.get("sources"):
            charts.append({
                "type": "pie_chart",
                "title": "Répartition des revenus par source",
                "data": revenue_analysis["sources"]
            })
        
        # Graphique des dépenses par catégorie
        expense_analysis = financial_analysis.get("expense_analysis", {})
        if expense_analysis.get("categories"):
            charts.append({
                "type": "bar_chart",
                "title": "Dépenses par catégorie",
                "data": expense_analysis["categories"]
            })
        
        return charts
    
    def _create_tax_charts(self, tax_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Créer des graphiques fiscaux"""
        charts = []
        
        # Graphique des obligations fiscales
        tax_summary = tax_analysis.get("tax_summary", {})
        if tax_summary:
            charts.append({
                "type": "donut_chart",
                "title": "Répartition des obligations fiscales",
                "data": {
                    "TPS": tax_summary.get("gst_remittance", 0),
                    "TVQ": tax_summary.get("qst_remittance", 0)
                }
            })
        
        return charts
    
    def _create_trend_graphs(self, trends_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Créer des graphiques de tendances"""
        graphs = []
        
        # Graphique de tendance des revenus
        revenue_trends = trends_analysis.get("revenue_trends", {})
        if revenue_trends:
            graphs.append({
                "type": "line_chart",
                "title": "Tendance des revenus",
                "data": revenue_trends
            })
        
        return graphs
    
    def _generate_financial_recommendations(self, financial_analysis: Dict[str, Any]) -> List[str]:
        """Générer des recommandations financières"""
        recommendations = []
        
        profitability = financial_analysis.get("profitability_analysis", {})
        if profitability.get("profit_margin", 0) < 10:
            recommendations.append("Optimiser la structure des coûts pour améliorer la marge")
        
        return recommendations
    
    def _generate_tax_recommendations(self, tax_analysis: Dict[str, Any]) -> List[str]:
        """Générer des recommandations fiscales"""
        recommendations = []
        
        optimization_opportunities = tax_analysis.get("optimization_opportunities", [])
        if optimization_opportunities:
            recommendations.append("Explorer les opportunités d'optimisation fiscale identifiées")
        
        return recommendations
    
    def _generate_compliance_recommendations(self, compliance_status: Dict[str, Any]) -> List[str]:
        """Générer des recommandations de conformité"""
        recommendations = []
        
        if compliance_status.get("upcoming_deadlines", 0) > 0:
            recommendations.append("Préparer les déclarations pour les échéances à venir")
        
        return recommendations
    
    def get_report_history(self) -> List[Dict[str, Any]]:
        """Obtenir l'historique des rapports"""
        return self.report_history
    
    def export_report(self, report: Dict[str, Any], format: str = "json") -> str:
        """Exporter un rapport dans différents formats"""
        if format.lower() == "json":
            import json
            return json.dumps(report, indent=2, default=str)
        elif format.lower() == "pdf":
            return "PDF export not implemented yet"
        elif format.lower() == "excel":
            return "Excel export not implemented yet"
        else:
            raise ValueError(f"Format non supporté: {format}")
    
    def create_dashboard_data(self, transactions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Créer des données pour tableau de bord"""
        return {
            "key_metrics": self._calculate_key_metrics(transactions),
            "recent_activity": self._get_recent_activity(transactions),
            "alerts": self._generate_dashboard_alerts(transactions),
            "charts": self._create_dashboard_charts(transactions)
        }
    
    def _calculate_key_metrics(self, transactions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculer les métriques clés"""
        total_revenue = sum(t.get('amount', 0) for t in transactions if t.get('type') == 'revenue')
        total_expenses = sum(t.get('amount', 0) for t in transactions if t.get('type') == 'expense')
        net_income = total_revenue - total_expenses
        
        return {
            "total_revenue": total_revenue,
            "total_expenses": total_expenses,
            "net_income": net_income,
            "profit_margin": (net_income / total_revenue * 100) if total_revenue > 0 else 0,
            "transaction_count": len(transactions)
        }
    
    def _get_recent_activity(self, transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Obtenir l'activité récente"""
        # Retourner les 10 dernières transactions
        return transactions[-10:] if len(transactions) > 10 else transactions
    
    def _generate_dashboard_alerts(self, transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Générer des alertes pour le tableau de bord"""
        alerts = []
        
        # Alerte pour transactions élevées
        high_amount_transactions = [t for t in transactions if t.get('amount', 0) > 5000]
        if high_amount_transactions:
            alerts.append({
                "type": "high_amount",
                "message": f"{len(high_amount_transactions)} transactions élevées détectées",
                "severity": "medium"
            })
        
        return alerts
    
    def _create_dashboard_charts(self, transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Créer des graphiques pour le tableau de bord"""
        charts = []
        
        # Graphique des revenus vs dépenses
        total_revenue = sum(t.get('amount', 0) for t in transactions if t.get('type') == 'revenue')
        total_expenses = sum(t.get('amount', 0) for t in transactions if t.get('type') == 'expense')
        
        charts.append({
            "type": "comparison_chart",
            "title": "Revenus vs Dépenses",
            "data": {
                "Revenus": total_revenue,
                "Dépenses": total_expenses
            }
        })
        
        return charts 
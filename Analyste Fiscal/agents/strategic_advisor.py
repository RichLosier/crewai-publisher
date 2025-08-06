"""
Agent Conseiller Stratégique - Consultant fiscal stratégique intelligent
"""
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from decimal import Decimal
from crewai import Agent
from config.settings import config
from config.tax_rules import tax_rules_engine
from config.fiscal_calendar import fiscal_calendar

class StrategicAdvisorAgent:
    """Agent spécialisé dans les conseils stratégiques fiscaux"""
    
    def __init__(self):
        self.agent = Agent(
            role="Consultant fiscal stratégique intelligent",
            goal="Fournir des conseils stratégiques personnalisés pour optimiser la situation fiscale avec un ROI maximal",
            backstory="""Vous êtes un consultant fiscal stratégique senior avec plus de 20 ans d'expérience 
            dans l'optimisation fiscale pour entreprises québécoises. Vous maîtrisez les stratégies fiscales 
            avancées, les crédits d'impôt, les déductions, et toutes les opportunités d'optimisation. 
            Votre mission est de fournir des conseils stratégiques personnalisés pour maximiser les économies 
            fiscales tout en maintenant la conformité.""",
            verbose=True,
            allow_delegation=False
        )
        
        # Initialiser les outils stratégiques
        self.tax_engine = tax_rules_engine
        self.calendar = fiscal_calendar
        
        # Historique des stratégies
        self.strategy_history = []
        self.optimization_opportunities = []
    
    def analyze_tax_optimization_opportunities(self, transactions: List[Dict[str, Any]], 
                                            company_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Analyser les opportunités d'optimisation fiscale"""
        analysis = {
            "current_situation": {},
            "optimization_opportunities": [],
            "strategic_recommendations": [],
            "roi_analysis": {},
            "implementation_plan": {}
        }
        
        # Analyser la situation actuelle
        current_situation = self._analyze_current_situation(transactions, company_profile)
        analysis["current_situation"] = current_situation
        
        # Identifier les opportunités
        opportunities = self._identify_optimization_opportunities(transactions, company_profile)
        analysis["optimization_opportunities"] = opportunities
        
        # Générer les recommandations stratégiques
        recommendations = self._generate_strategic_recommendations(opportunities, company_profile)
        analysis["strategic_recommendations"] = recommendations
        
        # Analyser le ROI
        roi_analysis = self._analyze_roi(opportunities, recommendations)
        analysis["roi_analysis"] = roi_analysis
        
        # Plan d'implémentation
        implementation_plan = self._create_implementation_plan(recommendations)
        analysis["implementation_plan"] = implementation_plan
        
        return analysis
    
    def _analyze_current_situation(self, transactions: List[Dict[str, Any]], 
                                 company_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Analyser la situation fiscale actuelle"""
        total_revenue = sum(t.get('amount', 0) for t in transactions if t.get('type') == 'revenue')
        total_expenses = sum(t.get('amount', 0) for t in transactions if t.get('type') == 'expense')
        net_income = total_revenue - total_expenses
        
        # Calculer les taxes actuelles
        current_taxes = self._calculate_current_taxes(transactions)
        
        # Analyser l'efficacité fiscale
        tax_efficiency = (current_taxes['total_tax'] / total_revenue) if total_revenue > 0 else 0
        
        return {
            "total_revenue": total_revenue,
            "total_expenses": total_expenses,
            "net_income": net_income,
            "current_taxes": current_taxes,
            "tax_efficiency": tax_efficiency,
            "company_type": company_profile.get('type', 'unknown'),
            "fiscal_year": config.get_current_fiscal_year()
        }
    
    def _identify_optimization_opportunities(self, transactions: List[Dict[str, Any]], 
                                          company_profile: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identifier les opportunités d'optimisation"""
        opportunities = []
        
        # Opportunités de déductions
        deduction_opportunities = self._find_deduction_opportunities(transactions, company_profile)
        opportunities.extend(deduction_opportunities)
        
        # Opportunités de crédits d'impôt
        credit_opportunities = self._find_credit_opportunities(transactions, company_profile)
        opportunities.extend(credit_opportunities)
        
        # Opportunités de structure
        structure_opportunities = self._find_structure_opportunities(company_profile)
        opportunities.extend(structure_opportunities)
        
        # Opportunités de timing
        timing_opportunities = self._find_timing_opportunities(transactions)
        opportunities.extend(timing_opportunities)
        
        return opportunities
    
    def _find_deduction_opportunities(self, transactions: List[Dict[str, Any]], 
                                    company_profile: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Trouver les opportunités de déductions"""
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
        
        # Opportunités de déductions d'entreprise
        if company_profile.get('type') == 'tech_startup':
            if expense_categories.get('software', 0) < 5000:
                opportunities.append({
                    "type": "deduction",
                    "category": "software_investment",
                    "description": "Investissement en logiciels pour déduction",
                    "potential_savings": 750,  # 15% de 5000
                    "implementation_cost": 5000,
                    "roi": 15,
                    "priority": "high"
                })
        
        # Opportunités de bureau à domicile
        if 'home_office' not in expense_categories:
            opportunities.append({
                "type": "deduction",
                "category": "home_office",
                "description": "Déduction bureau à domicile",
                "potential_savings": 500,
                "implementation_cost": 0,
                "roi": "infinite",
                "priority": "medium"
            })
        
        return opportunities
    
    def _find_credit_opportunities(self, transactions: List[Dict[str, Any]], 
                                 company_profile: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Trouver les opportunités de crédits d'impôt"""
        opportunities = []
        
        # Crédit SR&ED
        if company_profile.get('type') == 'tech_startup':
            r_d_expenses = sum(t.get('amount', 0) for t in transactions 
                             if t.get('type') == 'expense' and t.get('category') in ['research', 'development'])
            
            if r_d_expenses < 10000:
                opportunities.append({
                    "type": "credit",
                    "category": "sred",
                    "description": "Crédit d'impôt SR&ED",
                    "potential_savings": 3500,  # 35% de 10000
                    "implementation_cost": 10000,
                    "roi": 35,
                    "priority": "high"
                })
        
        # Crédit médias numériques (Québec)
        if company_profile.get('province') == 'QC':
            digital_media_expenses = sum(t.get('amount', 0) for t in transactions 
                                       if t.get('type') == 'expense' and t.get('category') == 'digital_media')
            
            if digital_media_expenses < 5000:
                opportunities.append({
                    "type": "credit",
                    "category": "digital_media_qc",
                    "description": "Crédit d'impôt médias numériques QC",
                    "potential_savings": 1200,  # 24% de 5000
                    "implementation_cost": 5000,
                    "roi": 24,
                    "priority": "medium"
                })
        
        return opportunities
    
    def _find_structure_opportunities(self, company_profile: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Trouver les opportunités de structure"""
        opportunities = []
        
        # Optimisation de structure pour petites entreprises
        if company_profile.get('revenue', 0) < 500000:
            opportunities.append({
                "type": "structure",
                "category": "small_business_deduction",
                "description": "Déduction pour petite entreprise",
                "potential_savings": 5000,
                "implementation_cost": 0,
                "roi": "infinite",
                "priority": "high"
            })
        
        # Optimisation de structure pour startups
        if company_profile.get('type') == 'tech_startup' and company_profile.get('age', 0) < 3:
            opportunities.append({
                "type": "structure",
                "category": "startup_incentives",
                "description": "Incitatifs pour startups",
                "potential_savings": 3000,
                "implementation_cost": 0,
                "roi": "infinite",
                "priority": "high"
            })
        
        return opportunities
    
    def _find_timing_opportunities(self, transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Trouver les opportunités de timing"""
        opportunities = []
        
        # Optimisation des achats en fin d'année
        current_month = datetime.now().month
        if current_month in [11, 12]:
            opportunities.append({
                "type": "timing",
                "category": "year_end_purchases",
                "description": "Achats en fin d'année pour déductions",
                "potential_savings": 2000,
                "implementation_cost": 10000,
                "roi": 20,
                "priority": "high"
            })
        
        return opportunities
    
    def _generate_strategic_recommendations(self, opportunities: List[Dict[str, Any]], 
                                         company_profile: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Générer des recommandations stratégiques"""
        recommendations = []
        
        # Trier les opportunités par ROI
        sorted_opportunities = sorted(opportunities, key=lambda x: x.get('roi', 0), reverse=True)
        
        for opportunity in sorted_opportunities[:5]:  # Top 5
            recommendation = {
                "opportunity": opportunity,
                "implementation_steps": self._get_implementation_steps(opportunity),
                "timeline": self._get_implementation_timeline(opportunity),
                "risks": self._assess_risks(opportunity),
                "success_metrics": self._define_success_metrics(opportunity)
            }
            recommendations.append(recommendation)
        
        return recommendations
    
    def _analyze_roi(self, opportunities: List[Dict[str, Any]], 
                    recommendations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyser le ROI des opportunités"""
        total_potential_savings = sum(opp.get('potential_savings', 0) for opp in opportunities)
        total_implementation_cost = sum(opp.get('implementation_cost', 0) for opp in opportunities)
        
        net_savings = total_potential_savings - total_implementation_cost
        overall_roi = (net_savings / total_implementation_cost * 100) if total_implementation_cost > 0 else float('inf')
        
        return {
            "total_potential_savings": total_potential_savings,
            "total_implementation_cost": total_implementation_cost,
            "net_savings": net_savings,
            "overall_roi": overall_roi,
            "opportunities_count": len(opportunities),
            "high_priority_count": len([opp for opp in opportunities if opp.get('priority') == 'high'])
        }
    
    def _create_implementation_plan(self, recommendations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Créer un plan d'implémentation"""
        plan = {
            "phases": [],
            "timeline": {},
            "resources_required": [],
            "milestones": [],
            "success_criteria": []
        }
        
        # Phase 1: Opportunités à haut ROI
        high_roi_recommendations = [r for r in recommendations if r['opportunity'].get('priority') == 'high']
        if high_roi_recommendations:
            plan["phases"].append({
                "phase": 1,
                "name": "Opportunités à haut ROI",
                "recommendations": high_roi_recommendations,
                "timeline": "1-2 mois",
                "expected_savings": sum(r['opportunity'].get('potential_savings', 0) for r in high_roi_recommendations)
            })
        
        # Phase 2: Opportunités à ROI moyen
        medium_roi_recommendations = [r for r in recommendations if r['opportunity'].get('priority') == 'medium']
        if medium_roi_recommendations:
            plan["phases"].append({
                "phase": 2,
                "name": "Opportunités à ROI moyen",
                "recommendations": medium_roi_recommendations,
                "timeline": "3-6 mois",
                "expected_savings": sum(r['opportunity'].get('potential_savings', 0) for r in medium_roi_recommendations)
            })
        
        return plan
    
    def _get_implementation_steps(self, opportunity: Dict[str, Any]) -> List[str]:
        """Obtenir les étapes d'implémentation pour une opportunité"""
        steps = []
        
        if opportunity['type'] == 'deduction':
            if opportunity['category'] == 'software_investment':
                steps = [
                    "Évaluer les besoins en logiciels",
                    "Rechercher les solutions appropriées",
                    "Obtenir les devis",
                    "Effectuer les achats",
                    "Documenter les dépenses"
                ]
            elif opportunity['category'] == 'home_office':
                steps = [
                    "Calculer le pourcentage d'utilisation",
                    "Mesurer l'espace utilisé",
                    "Documenter l'utilisation exclusive",
                    "Calculer les dépenses proportionnelles"
                ]
        
        elif opportunity['type'] == 'credit':
            if opportunity['category'] == 'sred':
                steps = [
                    "Identifier les activités de R&D",
                    "Documenter les projets éligibles",
                    "Calculer les dépenses éligibles",
                    "Préparer la documentation SR&ED"
                ]
        
        return steps
    
    def _get_implementation_timeline(self, opportunity: Dict[str, Any]) -> str:
        """Obtenir le timeline d'implémentation"""
        if opportunity['type'] == 'deduction':
            return "1-2 mois"
        elif opportunity['type'] == 'credit':
            return "3-6 mois"
        elif opportunity['type'] == 'structure':
            return "6-12 mois"
        else:
            return "Variable"
    
    def _assess_risks(self, opportunity: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Évaluer les risques d'une opportunité"""
        risks = []
        
        if opportunity['type'] == 'deduction':
            risks.append({
                "type": "audit_risk",
                "description": "Risque d'audit pour déductions",
                "severity": "low",
                "mitigation": "Documentation complète"
            })
        
        elif opportunity['type'] == 'credit':
            risks.append({
                "type": "eligibility_risk",
                "description": "Risque de non-éligibilité",
                "severity": "medium",
                "mitigation": "Vérification préalable"
            })
        
        return risks
    
    def _define_success_metrics(self, opportunity: Dict[str, Any]) -> List[str]:
        """Définir les métriques de succès"""
        metrics = [
            f"Économies réalisées: {opportunity.get('potential_savings', 0)}",
            f"ROI atteint: {opportunity.get('roi', 0)}%",
            "Conformité maintenue",
            "Documentation complète"
        ]
        
        return metrics
    
    def _calculate_current_taxes(self, transactions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculer les taxes actuelles"""
        total_revenue = sum(t.get('amount', 0) for t in transactions if t.get('type') == 'revenue')
        total_expenses = sum(t.get('amount', 0) for t in transactions if t.get('type') == 'expense')
        net_income = total_revenue - total_expenses
        
        # Calculs simplifiés
        federal_tax = net_income * 0.15
        provincial_tax = net_income * 0.1475
        total_tax = federal_tax + provincial_tax
        
        return {
            "federal_tax": federal_tax,
            "provincial_tax": provincial_tax,
            "total_tax": total_tax,
            "effective_rate": (total_tax / total_revenue * 100) if total_revenue > 0 else 0
        }
    
    def get_strategy_history(self) -> List[Dict[str, Any]]:
        """Obtenir l'historique des stratégies"""
        return self.strategy_history
    
    def save_strategy(self, strategy: Dict[str, Any]):
        """Sauvegarder une stratégie dans l'historique"""
        strategy['timestamp'] = datetime.now().isoformat()
        self.strategy_history.append(strategy)
    
    def get_benchmark_comparison(self, company_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Comparer avec les benchmarks du secteur"""
        # À implémenter avec des données de benchmark
        return {
            "sector": company_profile.get('sector', 'unknown'),
            "company_size": company_profile.get('size', 'unknown'),
            "benchmark_tax_rate": 25.0,  # Exemple
            "company_tax_rate": 20.0,    # Exemple
            "optimization_potential": 5.0
        } 
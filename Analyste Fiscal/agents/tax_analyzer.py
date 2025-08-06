"""
Agent Analyseur Fiscal - Spécialiste en analyse fiscale québécoise et canadienne
"""
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from decimal import Decimal
from crewai import Agent
from config.settings import config
from config.tax_rules import tax_rules_engine
from config.fiscal_calendar import fiscal_calendar

class TaxAnalyzerAgent:
    """Agent spécialisé dans l'analyse fiscale québécoise et canadienne"""
    
    def __init__(self):
        self.agent = Agent(
            role="Spécialiste en analyse fiscale québécoise et canadienne",
            goal="Analyser les implications fiscales de chaque transaction et calculer les obligations avec une précision de 99.9%",
            backstory="""Vous êtes un expert fiscal québécois et canadien avec plus de 15 ans d'expérience 
            dans l'analyse fiscale pour entreprises. Vous maîtrisez parfaitement les règles de TPS/TVH, 
            les déductions d'entreprise, les crédits d'impôt, et toutes les nuances fiscales québécoises 
            et canadiennes. Votre mission est d'analyser chaque transaction et de calculer précisément 
            toutes les obligations fiscales.""",
            verbose=True,
            allow_delegation=False
        )
        
        # Initialiser les outils d'analyse
        self.tax_engine = tax_rules_engine
        self.calendar = fiscal_calendar
    
    def analyze_transactions(self, transactions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyser toutes les transactions pour les implications fiscales"""
        analysis_results = {
            "summary": {},
            "gst_analysis": {},
            "qst_analysis": {},
            "income_tax_analysis": {},
            "deductions": [],
            "credits": [],
            "obligations": [],
            "recommendations": []
        }
        
        # Analyser les taxes de vente
        gst_qst_analysis = self._analyze_sales_taxes(transactions)
        analysis_results["gst_analysis"] = gst_qst_analysis["gst"]
        analysis_results["qst_analysis"] = gst_qst_analysis["qst"]
        
        # Analyser l'impôt sur le revenu
        income_tax_analysis = self._analyze_income_tax(transactions)
        analysis_results["income_tax_analysis"] = income_tax_analysis
        
        # Calculer les déductions
        deductions = self._calculate_deductions(transactions)
        analysis_results["deductions"] = deductions
        
        # Calculer les crédits d'impôt
        credits = self._calculate_credits(transactions)
        analysis_results["credits"] = credits
        
        # Déterminer les obligations
        obligations = self._determine_obligations(analysis_results)
        analysis_results["obligations"] = obligations
        
        # Générer les recommandations
        recommendations = self._generate_recommendations(analysis_results)
        analysis_results["recommendations"] = recommendations
        
        # Résumé général
        analysis_results["summary"] = self._create_summary(analysis_results)
        
        return analysis_results
    
    def _analyze_sales_taxes(self, transactions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyser les taxes de vente (TPS/TVH)"""
        gst_collected = Decimal('0')
        gst_paid = Decimal('0')
        qst_collected = Decimal('0')
        qst_paid = Decimal('0')
        taxable_revenue = Decimal('0')
        taxable_expenses = Decimal('0')
        
        for transaction in transactions:
            amount = Decimal(str(transaction.get('amount', 0)))
            transaction_type = transaction.get('type', '')
            
            if transaction_type == 'revenue':
                taxable_revenue += amount
                # Calculer taxes collectées
                taxes = self.tax_engine.calculate_combined_taxes(amount)
                gst_collected += taxes['gst'].tax_amount
                qst_collected += taxes['qst'].tax_amount
                
            elif transaction_type == 'expense':
                taxable_expenses += amount
                # Calculer taxes payées
                taxes = self.tax_engine.calculate_combined_taxes(amount)
                gst_paid += taxes['gst'].tax_amount
                qst_paid += taxes['qst'].tax_amount
        
        gst_remittance = gst_collected - gst_paid
        qst_remittance = qst_collected - qst_paid
        
        return {
            "gst": {
                "collected": float(gst_collected),
                "paid": float(gst_paid),
                "remittance": float(gst_remittance),
                "rate": 0.05,
                "taxable_revenue": float(taxable_revenue)
            },
            "qst": {
                "collected": float(qst_collected),
                "paid": float(qst_paid),
                "remittance": float(qst_remittance),
                "rate": 0.09975,
                "taxable_revenue": float(taxable_revenue)
            }
        }
    
    def _analyze_income_tax(self, transactions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyser l'impôt sur le revenu"""
        total_revenue = Decimal('0')
        total_expenses = Decimal('0')
        net_income = Decimal('0')
        
        for transaction in transactions:
            amount = Decimal(str(transaction.get('amount', 0)))
            transaction_type = transaction.get('type', '')
            
            if transaction_type == 'revenue':
                total_revenue += amount
            elif transaction_type == 'expense':
                total_expenses += amount
        
        net_income = total_revenue - total_expenses
        
        # Calculer l'impôt estimé (taux simplifiés)
        federal_tax_rate = 0.15  # Taux fédéral de base
        provincial_tax_rate = 0.1475  # Taux québécois de base
        
        federal_tax = net_income * Decimal(str(federal_tax_rate))
        provincial_tax = net_income * Decimal(str(provincial_tax_rate))
        total_tax = federal_tax + provincial_tax
        
        return {
            "total_revenue": float(total_revenue),
            "total_expenses": float(total_expenses),
            "net_income": float(net_income),
            "federal_tax": float(federal_tax),
            "provincial_tax": float(provincial_tax),
            "total_tax": float(total_tax),
            "federal_rate": federal_tax_rate,
            "provincial_rate": provincial_tax_rate
        }
    
    def _calculate_deductions(self, transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Calculer toutes les déductions disponibles"""
        deductions = []
        
        # Analyser les dépenses par catégorie
        expense_categories = {}
        for transaction in transactions:
            if transaction.get('type') == 'expense':
                amount = Decimal(str(transaction.get('amount', 0)))
                category = transaction.get('category', 'other')
                
                if category not in expense_categories:
                    expense_categories[category] = Decimal('0')
                
                expense_categories[category] += amount
        
        # Appliquer les règles de déduction
        deduction_rules = self.tax_engine.get_active_rules(category="deduction")
        
        for category, amount in expense_categories.items():
            for rule in deduction_rules:
                if self._check_deduction_eligibility(category, amount, rule):
                    deduction_amount = amount * Decimal(str(rule.value))
                    deductions.append({
                        "category": category,
                        "rule": rule.name,
                        "description": rule.description,
                        "amount": float(amount),
                        "deduction_amount": float(deduction_amount),
                        "rate": rule.value
                    })
        
        return deductions
    
    def _calculate_credits(self, transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Calculer tous les crédits d'impôt disponibles"""
        credits = []
        
        # Analyser les dépenses éligibles
        eligible_expenses = []
        for transaction in transactions:
            if transaction.get('type') == 'expense':
                category = transaction.get('category', '')
                if category in ['research', 'development', 'rd', 'digital_media']:
                    eligible_expenses.append(transaction)
        
        # Appliquer les règles de crédit
        credit_rules = self.tax_engine.get_active_rules(category="credit")
        
        for expense in eligible_expenses:
            amount = Decimal(str(expense.get('amount', 0)))
            category = expense.get('category', '')
            
            for rule in credit_rules:
                if self._check_credit_eligibility(category, amount, rule):
                    credit_amount = amount * Decimal(str(rule.value))
                    credits.append({
                        "category": category,
                        "rule": rule.name,
                        "description": rule.description,
                        "expense_amount": float(amount),
                        "credit_amount": float(credit_amount),
                        "rate": rule.value
                    })
        
        return credits
    
    def _determine_obligations(self, analysis_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Déterminer toutes les obligations fiscales"""
        obligations = []
        
        # Obligations TPS/TVH
        gst_analysis = analysis_results["gst_analysis"]
        qst_analysis = analysis_results["qst_analysis"]
        
        if gst_analysis["remittance"] != 0:
            obligations.append({
                "type": "gst_remittance",
                "description": "Remise TPS",
                "amount": gst_analysis["remittance"],
                "deadline": self._get_next_gst_deadline(),
                "jurisdiction": "CA",
                "priority": "high"
            })
        
        if qst_analysis["remittance"] != 0:
            obligations.append({
                "type": "qst_remittance",
                "description": "Remise TVQ",
                "amount": qst_analysis["remittance"],
                "deadline": self._get_next_qst_deadline(),
                "jurisdiction": "QC",
                "priority": "high"
            })
        
        # Obligations d'impôt sur le revenu
        income_tax = analysis_results["income_tax_analysis"]
        if income_tax["total_tax"] > 0:
            obligations.append({
                "type": "income_tax",
                "description": "Impôt sur le revenu",
                "amount": income_tax["total_tax"],
                "deadline": self._get_next_income_tax_deadline(),
                "jurisdiction": "both",
                "priority": "high"
            })
        
        return obligations
    
    def _generate_recommendations(self, analysis_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Générer des recommandations fiscales"""
        recommendations = []
        
        # Recommandations basées sur les déductions
        total_deductions = sum(d["deduction_amount"] for d in analysis_results["deductions"])
        if total_deductions < 1000:  # Seuil arbitraire
            recommendations.append({
                "type": "deduction_optimization",
                "description": "Considérer des dépenses supplémentaires pour optimiser les déductions",
                "priority": "medium",
                "potential_savings": "Variable"
            })
        
        # Recommandations basées sur les crédits
        total_credits = sum(c["credit_amount"] for c in analysis_results["credits"])
        if total_credits < 500:  # Seuil arbitraire
            recommendations.append({
                "type": "credit_optimization",
                "description": "Explorer les crédits d'impôt pour R&D et médias numériques",
                "priority": "high",
                "potential_savings": "Significatif"
            })
        
        # Recommandations basées sur les obligations
        upcoming_deadlines = self.calendar.get_upcoming_deadlines(30)
        if upcoming_deadlines:
            recommendations.append({
                "type": "deadline_reminder",
                "description": f"Échéances fiscales à venir: {len(upcoming_deadlines)}",
                "priority": "high",
                "deadlines": [d.name for d in upcoming_deadlines]
            })
        
        return recommendations
    
    def _create_summary(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Créer un résumé de l'analyse fiscale"""
        gst_analysis = analysis_results["gst_analysis"]
        qst_analysis = analysis_results["qst_analysis"]
        income_tax = analysis_results["income_tax_analysis"]
        
        total_tax_obligations = (
            gst_analysis["remittance"] + 
            qst_analysis["remittance"] + 
            income_tax["total_tax"]
        )
        
        total_deductions = sum(d["deduction_amount"] for d in analysis_results["deductions"])
        total_credits = sum(c["credit_amount"] for c in analysis_results["credits"])
        
        return {
            "total_tax_obligations": total_tax_obligations,
            "total_deductions": total_deductions,
            "total_credits": total_credits,
            "net_tax_liability": total_tax_obligations - total_credits,
            "analysis_date": datetime.now().isoformat(),
            "fiscal_period": config.get_fiscal_period()
        }
    
    def _check_deduction_eligibility(self, category: str, amount: Decimal, rule: Any) -> bool:
        """Vérifier l'éligibilité pour une déduction"""
        # Logique simplifiée - à étendre selon les besoins
        if rule.name == "Business_Expense_Deduction":
            return category in ["office_supplies", "utilities", "rent", "marketing"]
        elif rule.name == "Home_Office_Deduction":
            return category == "home_office"
        elif rule.name == "Tech_Startup_Deduction":
            return category in ["software", "equipment", "development"]
        
        return False
    
    def _check_credit_eligibility(self, category: str, amount: Decimal, rule: Any) -> bool:
        """Vérifier l'éligibilité pour un crédit d'impôt"""
        if rule.name == "SRED_Credit":
            return category in ["research", "development", "rd"]
        elif rule.name == "Digital_Media_Credit_QC":
            return category == "digital_media"
        
        return False
    
    def _get_next_gst_deadline(self) -> Optional[datetime]:
        """Obtenir la prochaine échéance TPS"""
        deadlines = self.calendar.get_deadlines_by_type("quarterly")
        for deadline in deadlines:
            if "TPS" in deadline.name:
                return deadline.date
        return None
    
    def _get_next_qst_deadline(self) -> Optional[datetime]:
        """Obtenir la prochaine échéance TVQ"""
        deadlines = self.calendar.get_deadlines_by_type("quarterly")
        for deadline in deadlines:
            if "TVH" in deadline.name:
                return deadline.date
        return None
    
    def _get_next_income_tax_deadline(self) -> Optional[datetime]:
        """Obtenir la prochaine échéance d'impôt sur le revenu"""
        deadlines = self.calendar.get_deadlines_by_type("annual")
        for deadline in deadlines:
            if "revenus" in deadline.name:
                return deadline.date
        return None
    
    def get_tax_forecast(self, months_ahead: int = 12) -> Dict[str, Any]:
        """Prévoir les obligations fiscales futures"""
        # Logique de prévision basée sur les tendances historiques
        # À implémenter avec des données historiques
        return {
            "forecast_period": f"{months_ahead} mois",
            "estimated_gst_obligations": [],
            "estimated_qst_obligations": [],
            "estimated_income_tax": [],
            "confidence_level": "medium"
        }
    
    def analyze_tax_efficiency(self, transactions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyser l'efficacité fiscale de l'entreprise"""
        analysis = self.analyze_transactions(transactions)
        
        total_revenue = analysis["income_tax_analysis"]["total_revenue"]
        total_tax = analysis["summary"]["total_tax_obligations"]
        
        tax_efficiency_ratio = (total_tax / total_revenue) if total_revenue > 0 else 0
        
        return {
            "tax_efficiency_ratio": tax_efficiency_ratio,
            "effective_tax_rate": tax_efficiency_ratio * 100,
            "optimization_opportunities": analysis["recommendations"],
            "benchmark_comparison": "À implémenter"
        } 
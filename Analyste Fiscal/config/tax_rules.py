"""
Règles fiscales dynamiques pour le Québec et le Canada
"""
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime, date
from decimal import Decimal
import json
from config.settings import config

@dataclass
class TaxRule:
    """Règle fiscale"""
    name: str
    description: str
    jurisdiction: str  # 'QC', 'CA', 'both'
    category: str  # 'deduction', 'credit', 'rate', 'threshold'
    value: Any
    conditions: Dict[str, Any] = None
    effective_date: date = None
    expiry_date: date = None
    is_active: bool = True

@dataclass
class TaxCalculation:
    """Résultat d'un calcul fiscal"""
    base_amount: Decimal
    tax_amount: Decimal
    rate_applied: float
    deductions: List[Dict[str, Any]]
    credits: List[Dict[str, Any]]
    net_amount: Decimal
    jurisdiction: str

class TaxRulesEngine:
    """Moteur de règles fiscales dynamiques"""
    
    def __init__(self):
        self.rules: Dict[str, TaxRule] = {}
        self.load_default_rules()
    
    def load_default_rules(self):
        """Charger les règles fiscales par défaut"""
        
        # Règles de taux de taxes
        self.add_rule(TaxRule(
            name="TPS_Rate",
            description="Taux de TPS (Taxe sur les Produits et Services)",
            jurisdiction="CA",
            category="rate",
            value=0.05,  # 5%
            effective_date=date(2008, 1, 1)
        ))
        
        self.add_rule(TaxRule(
            name="TVQ_Rate",
            description="Taux de TVQ (Taxe de Vente du Québec)",
            jurisdiction="QC",
            category="rate",
            value=0.09975,  # 9.975%
            effective_date=date(2013, 1, 1)
        ))
        
        # Seuils et limites
        self.add_rule(TaxRule(
            name="Small_Business_Threshold",
            description="Seuil pour petite entreprise",
            jurisdiction="both",
            category="threshold",
            value=30000.0,
            effective_date=date(2020, 1, 1)
        ))
        
        self.add_rule(TaxRule(
            name="QST_Registration_Threshold",
            description="Seuil d'inscription TVQ",
            jurisdiction="QC",
            category="threshold",
            value=30000.0,
            effective_date=date(2020, 1, 1)
        ))
        
        # Déductions d'entreprise
        self.add_rule(TaxRule(
            name="Business_Expense_Deduction",
            description="Déduction pour dépenses d'entreprise",
            jurisdiction="both",
            category="deduction",
            value=1.0,  # 100% déductible
            conditions={"expense_type": "business", "documented": True}
        ))
        
        self.add_rule(TaxRule(
            name="Home_Office_Deduction",
            description="Déduction bureau à domicile",
            jurisdiction="both",
            category="deduction",
            value=0.25,  # 25% des dépenses
            conditions={"home_office_percentage": ">0", "exclusive_use": True}
        ))
        
        # Crédits d'impôt
        self.add_rule(TaxRule(
            name="SRED_Credit",
            description="Crédit d'impôt pour R&D",
            jurisdiction="both",
            category="credit",
            value=0.35,  # 35% des dépenses
            conditions={"sred_eligible": True, "documented": True}
        ))
        
        self.add_rule(TaxRule(
            name="Digital_Media_Credit_QC",
            description="Crédit d'impôt pour médias numériques QC",
            jurisdiction="QC",
            category="credit",
            value=0.24,  # 24% des dépenses
            conditions={"digital_media_eligible": True, "qc_resident": True}
        ))
        
        # Règles spéciales pour iFiveMe
        self.add_rule(TaxRule(
            name="Tech_Startup_Deduction",
            description="Déduction spéciale pour startup technologique",
            jurisdiction="both",
            category="deduction",
            value=0.15,  # 15% supplémentaire
            conditions={"company_type": "tech_startup", "revenue": "<100000"}
        ))
    
    def add_rule(self, rule: TaxRule):
        """Ajouter une règle fiscale"""
        self.rules[rule.name] = rule
    
    def get_rule(self, name: str) -> Optional[TaxRule]:
        """Obtenir une règle par nom"""
        return self.rules.get(name)
    
    def get_active_rules(self, jurisdiction: str = None, category: str = None) -> List[TaxRule]:
        """Obtenir les règles actives filtrées"""
        active_rules = []
        
        for rule in self.rules.values():
            if not rule.is_active:
                continue
                
            if jurisdiction and rule.jurisdiction not in [jurisdiction, 'both']:
                continue
                
            if category and rule.category != category:
                continue
                
            # Vérifier les dates d'effet
            today = date.today()
            if rule.effective_date and today < rule.effective_date:
                continue
            if rule.expiry_date and today > rule.expiry_date:
                continue
                
            active_rules.append(rule)
        
        return active_rules
    
    def calculate_gst(self, amount: Decimal, is_zero_rated: bool = False) -> TaxCalculation:
        """Calculer la TPS"""
        if is_zero_rated:
            return TaxCalculation(
                base_amount=amount,
                tax_amount=Decimal('0'),
                rate_applied=0.0,
                deductions=[],
                credits=[],
                net_amount=amount,
                jurisdiction="CA"
            )
        
        gst_rate = self.get_rule("TPS_Rate").value
        tax_amount = amount * Decimal(str(gst_rate))
        
        return TaxCalculation(
            base_amount=amount,
            tax_amount=tax_amount,
            rate_applied=gst_rate,
            deductions=[],
            credits=[],
            net_amount=amount + tax_amount,
            jurisdiction="CA"
        )
    
    def calculate_qst(self, amount: Decimal, is_zero_rated: bool = False) -> TaxCalculation:
        """Calculer la TVQ"""
        if is_zero_rated:
            return TaxCalculation(
                base_amount=amount,
                tax_amount=Decimal('0'),
                rate_applied=0.0,
                deductions=[],
                credits=[],
                net_amount=amount,
                jurisdiction="QC"
            )
        
        qst_rate = self.get_rule("TVQ_Rate").value
        tax_amount = amount * Decimal(str(qst_rate))
        
        return TaxCalculation(
            base_amount=amount,
            tax_amount=tax_amount,
            rate_applied=qst_rate,
            deductions=[],
            credits=[],
            net_amount=amount + tax_amount,
            jurisdiction="QC"
        )
    
    def calculate_combined_taxes(self, amount: Decimal, is_zero_rated: bool = False) -> Dict[str, TaxCalculation]:
        """Calculer TPS et TVQ combinées"""
        gst_calc = self.calculate_gst(amount, is_zero_rated)
        qst_calc = self.calculate_qst(amount, is_zero_rated)
        
        return {
            "gst": gst_calc,
            "qst": qst_calc,
            "total_tax": gst_calc.tax_amount + qst_calc.tax_amount,
            "total_amount": amount + gst_calc.tax_amount + qst_calc.tax_amount
        }
    
    def apply_deductions(self, amount: Decimal, expenses: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Appliquer les déductions disponibles"""
        deductions = []
        deduction_rules = self.get_active_rules(category="deduction")
        
        for expense in expenses:
            for rule in deduction_rules:
                if self._check_conditions(expense, rule.conditions):
                    deduction_amount = amount * Decimal(str(rule.value))
                    deductions.append({
                        "rule": rule.name,
                        "description": rule.description,
                        "amount": deduction_amount,
                        "rate": rule.value
                    })
        
        return deductions
    
    def apply_credits(self, tax_amount: Decimal, eligible_expenses: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Appliquer les crédits d'impôt disponibles"""
        credits = []
        credit_rules = self.get_active_rules(category="credit")
        
        for expense in eligible_expenses:
            for rule in credit_rules:
                if self._check_conditions(expense, rule.conditions):
                    credit_amount = tax_amount * Decimal(str(rule.value))
                    credits.append({
                        "rule": rule.name,
                        "description": rule.description,
                        "amount": credit_amount,
                        "rate": rule.value
                    })
        
        return credits
    
    def _check_conditions(self, data: Dict[str, Any], conditions: Dict[str, Any]) -> bool:
        """Vérifier si les conditions d'une règle sont remplies"""
        if not conditions:
            return True
        
        for key, value in conditions.items():
            if key not in data:
                return False
            
            if isinstance(value, str) and value.startswith(">"):
                # Comparaison numérique
                threshold = float(value[1:])
                if not isinstance(data[key], (int, float, Decimal)):
                    return False
                if float(data[key]) <= threshold:
                    return False
            elif isinstance(value, str) and value.startswith("<"):
                # Comparaison numérique
                threshold = float(value[1:])
                if not isinstance(data[key], (int, float, Decimal)):
                    return False
                if float(data[key]) >= threshold:
                    return False
            elif data[key] != value:
                return False
        
        return True
    
    def get_tax_summary(self, transactions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Générer un résumé fiscal complet"""
        total_revenue = Decimal('0')
        total_expenses = Decimal('0')
        total_gst_collected = Decimal('0')
        total_qst_collected = Decimal('0')
        total_gst_paid = Decimal('0')
        total_qst_paid = Decimal('0')
        
        for transaction in transactions:
            amount = Decimal(str(transaction.get('amount', 0)))
            transaction_type = transaction.get('type', 'revenue')
            
            if transaction_type == 'revenue':
                total_revenue += amount
                # Calculer taxes collectées
                taxes = self.calculate_combined_taxes(amount)
                total_gst_collected += taxes['gst'].tax_amount
                total_qst_collected += taxes['qst'].tax_amount
            elif transaction_type == 'expense':
                total_expenses += amount
                # Calculer taxes payées
                taxes = self.calculate_combined_taxes(amount)
                total_gst_paid += taxes['gst'].tax_amount
                total_qst_paid += taxes['qst'].tax_amount
        
        # Calculer les obligations fiscales
        gst_remittance = total_gst_collected - total_gst_paid
        qst_remittance = total_qst_collected - total_qst_paid
        
        return {
            "total_revenue": total_revenue,
            "total_expenses": total_expenses,
            "net_income": total_revenue - total_expenses,
            "gst_collected": total_gst_collected,
            "gst_paid": total_gst_paid,
            "gst_remittance": gst_remittance,
            "qst_collected": total_qst_collected,
            "qst_paid": total_qst_paid,
            "qst_remittance": qst_remittance,
            "total_tax_remittance": gst_remittance + qst_remittance
        }
    
    def update_rule(self, rule_name: str, new_value: Any, effective_date: date = None):
        """Mettre à jour une règle fiscale"""
        if rule_name in self.rules:
            rule = self.rules[rule_name]
            rule.value = new_value
            if effective_date:
                rule.effective_date = effective_date
    
    def export_rules(self, filepath: str):
        """Exporter les règles vers un fichier JSON"""
        rules_data = {}
        for name, rule in self.rules.items():
            rules_data[name] = {
                "name": rule.name,
                "description": rule.description,
                "jurisdiction": rule.jurisdiction,
                "category": rule.category,
                "value": rule.value,
                "conditions": rule.conditions,
                "effective_date": rule.effective_date.isoformat() if rule.effective_date else None,
                "expiry_date": rule.expiry_date.isoformat() if rule.expiry_date else None,
                "is_active": rule.is_active
            }
        
        with open(filepath, 'w') as f:
            json.dump(rules_data, f, indent=2)
    
    def import_rules(self, filepath: str):
        """Importer les règles depuis un fichier JSON"""
        with open(filepath, 'r') as f:
            rules_data = json.load(f)
        
        for name, data in rules_data.items():
            rule = TaxRule(
                name=data["name"],
                description=data["description"],
                jurisdiction=data["jurisdiction"],
                category=data["category"],
                value=data["value"],
                conditions=data["conditions"],
                effective_date=date.fromisoformat(data["effective_date"]) if data["effective_date"] else None,
                expiry_date=date.fromisoformat(data["expiry_date"]) if data["expiry_date"] else None,
                is_active=data["is_active"]
            )
            self.rules[name] = rule

# Instance globale du moteur de règles fiscales
tax_rules_engine = TaxRulesEngine() 
"""
Agent Processeur de Documents - Expert en traitement et génération de documents fiscaux
"""
from typing import Dict, List, Any, Optional
from datetime import datetime
import json
import os
from crewai import Agent
from config.settings import config
from config.tax_rules import tax_rules_engine
from config.fiscal_calendar import fiscal_calendar

class DocumentProcessorAgent:
    """Agent spécialisé dans le traitement et la génération de documents fiscaux"""
    
    def __init__(self):
        self.agent = Agent(
            role="Expert en traitement et génération de documents fiscaux",
            goal="Automatiser la création et soumission de tous documents fiscaux avec une précision de 100%",
            backstory="""Vous êtes un expert en documentation fiscale avec plus de 15 ans d'expérience 
            dans la préparation de déclarations fiscales québécoises et canadiennes. Vous maîtrisez 
            parfaitement tous les formulaires fiscaux, les exigences de documentation, et les processus 
            de soumission électronique. Votre mission est d'automatiser complètement la génération et 
            la soumission de tous les documents fiscaux requis.""",
            verbose=True,
            allow_delegation=False
        )
        
        # Initialiser les outils de traitement
        self.tax_engine = tax_rules_engine
        self.calendar = fiscal_calendar
        
        # Templates de documents
        self.templates_path = config.templates_path
        self._load_templates()
    
    def _load_templates(self):
        """Charger les templates de documents"""
        self.templates = {
            "gst_return": self._load_template("gst_return_template.json"),
            "qst_return": self._load_template("qst_return_template.json"),
            "t1_return": self._load_template("t1_return_template.json"),
            "tp1_return": self._load_template("tp1_return_template.json"),
            "t2_return": self._load_template("t2_return_template.json")
        }
    
    def _load_template(self, template_name: str) -> Dict[str, Any]:
        """Charger un template spécifique"""
        template_path = os.path.join(self.templates_path, template_name)
        try:
            with open(template_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            # Retourner un template par défaut
            return self._get_default_template(template_name)
    
    def _get_default_template(self, template_name: str) -> Dict[str, Any]:
        """Obtenir un template par défaut"""
        if "gst" in template_name:
            return {
                "form_type": "GST34",
                "period": "quarterly",
                "fields": {
                    "total_revenue": 0,
                    "gst_collected": 0,
                    "gst_paid": 0,
                    "gst_remittance": 0
                }
            }
        elif "qst" in template_name:
            return {
                "form_type": "TVQ-34",
                "period": "quarterly",
                "fields": {
                    "total_revenue": 0,
                    "qst_collected": 0,
                    "qst_paid": 0,
                    "qst_remittance": 0
                }
            }
        else:
            return {"form_type": "unknown", "fields": {}}
    
    def generate_tax_forms(self, transactions: List[Dict[str, Any]], 
                          period: str = "current_quarter") -> Dict[str, Any]:
        """Générer tous les formulaires fiscaux requis"""
        forms = {}
        
        # Analyser les transactions pour les données fiscales
        tax_data = self._extract_tax_data(transactions)
        
        # Générer les formulaires TPS/TVH
        if tax_data["gst_remittance"] != 0 or tax_data["qst_remittance"] != 0:
            forms["gst_return"] = self._generate_gst_return(tax_data, period)
            forms["qst_return"] = self._generate_qst_return(tax_data, period)
        
        # Générer les formulaires de revenus
        if period == "annual":
            forms["t1_return"] = self._generate_t1_return(tax_data)
            forms["tp1_return"] = self._generate_tp1_return(tax_data)
        
        return forms
    
    def _extract_tax_data(self, transactions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Extraire les données fiscales des transactions"""
        tax_data = {
            "total_revenue": 0,
            "total_expenses": 0,
            "gst_collected": 0,
            "gst_paid": 0,
            "qst_collected": 0,
            "qst_paid": 0,
            "deductible_expenses": 0,
            "capital_expenses": 0
        }
        
        for transaction in transactions:
            amount = transaction.get('amount', 0)
            transaction_type = transaction.get('type', '')
            
            if transaction_type == 'revenue':
                tax_data["total_revenue"] += amount
                # Calculer taxes collectées
                taxes = self.tax_engine.calculate_combined_taxes(amount)
                tax_data["gst_collected"] += taxes['gst'].tax_amount
                tax_data["qst_collected"] += taxes['qst'].tax_amount
                
            elif transaction_type == 'expense':
                tax_data["total_expenses"] += amount
                # Calculer taxes payées
                taxes = self.tax_engine.calculate_combined_taxes(amount)
                tax_data["gst_paid"] += taxes['gst'].tax_amount
                tax_data["qst_paid"] += taxes['qst'].tax_amount
                
                # Catégoriser les dépenses
                category = transaction.get('category', '')
                if category in ['office_supplies', 'utilities', 'rent']:
                    tax_data["deductible_expenses"] += amount
                elif category in ['equipment', 'software', 'furniture']:
                    tax_data["capital_expenses"] += amount
        
        # Calculer les remises
        tax_data["gst_remittance"] = tax_data["gst_collected"] - tax_data["gst_paid"]
        tax_data["qst_remittance"] = tax_data["qst_collected"] - tax_data["qst_paid"]
        
        return tax_data
    
    def _generate_gst_return(self, tax_data: Dict[str, Any], period: str) -> Dict[str, Any]:
        """Générer le formulaire TPS"""
        template = self.templates["gst_return"]
        
        form_data = {
            "form_type": "GST34",
            "period": period,
            "company_info": {
                "name": config.company.name,
                "gst_number": config.company.gst_number,
                "fiscal_year": config.get_current_fiscal_year()
            },
            "fields": {
                "total_revenue": tax_data["total_revenue"],
                "gst_collected": tax_data["gst_collected"],
                "gst_paid": tax_data["gst_paid"],
                "gst_remittance": tax_data["gst_remittance"]
            },
            "calculation_summary": {
                "line_101": tax_data["total_revenue"],
                "line_103": tax_data["gst_collected"],
                "line_104": tax_data["gst_paid"],
                "line_105": tax_data["gst_remittance"]
            }
        }
        
        return form_data
    
    def _generate_qst_return(self, tax_data: Dict[str, Any], period: str) -> Dict[str, Any]:
        """Générer le formulaire TVQ"""
        template = self.templates["qst_return"]
        
        form_data = {
            "form_type": "TVQ-34",
            "period": period,
            "company_info": {
                "name": config.company.name,
                "qst_number": config.company.qst_number,
                "fiscal_year": config.get_current_fiscal_year()
            },
            "fields": {
                "total_revenue": tax_data["total_revenue"],
                "qst_collected": tax_data["qst_collected"],
                "qst_paid": tax_data["qst_paid"],
                "qst_remittance": tax_data["qst_remittance"]
            },
            "calculation_summary": {
                "line_101": tax_data["total_revenue"],
                "line_103": tax_data["qst_collected"],
                "line_104": tax_data["qst_paid"],
                "line_105": tax_data["qst_remittance"]
            }
        }
        
        return form_data
    
    def _generate_t1_return(self, tax_data: Dict[str, Any]) -> Dict[str, Any]:
        """Générer le formulaire T1 (revenus fédéral)"""
        template = self.templates["t1_return"]
        
        net_income = tax_data["total_revenue"] - tax_data["total_expenses"]
        federal_tax = net_income * 0.15  # Taux simplifié
        
        form_data = {
            "form_type": "T1",
            "period": "annual",
            "company_info": {
                "name": config.company.name,
                "sin": "N/A",  # Pour entreprise
                "fiscal_year": config.get_current_fiscal_year()
            },
            "fields": {
                "total_revenue": tax_data["total_revenue"],
                "total_expenses": tax_data["total_expenses"],
                "net_income": net_income,
                "federal_tax": federal_tax,
                "deductible_expenses": tax_data["deductible_expenses"]
            }
        }
        
        return form_data
    
    def _generate_tp1_return(self, tax_data: Dict[str, Any]) -> Dict[str, Any]:
        """Générer le formulaire TP-1 (revenus québécois)"""
        template = self.templates["tp1_return"]
        
        net_income = tax_data["total_revenue"] - tax_data["total_expenses"]
        provincial_tax = net_income * 0.1475  # Taux simplifié
        
        form_data = {
            "form_type": "TP-1",
            "period": "annual",
            "company_info": {
                "name": config.company.name,
                "sin": "N/A",  # Pour entreprise
                "fiscal_year": config.get_current_fiscal_year()
            },
            "fields": {
                "total_revenue": tax_data["total_revenue"],
                "total_expenses": tax_data["total_expenses"],
                "net_income": net_income,
                "provincial_tax": provincial_tax,
                "deductible_expenses": tax_data["deductible_expenses"]
            }
        }
        
        return form_data
    
    def validate_forms(self, forms: Dict[str, Any]) -> Dict[str, Any]:
        """Valider les formulaires générés"""
        validation_results = {
            "overall_status": "valid",
            "forms_validated": [],
            "errors": [],
            "warnings": []
        }
        
        for form_name, form_data in forms.items():
            form_validation = self._validate_single_form(form_name, form_data)
            validation_results["forms_validated"].append(form_validation)
            
            if form_validation["status"] == "error":
                validation_results["overall_status"] = "error"
                validation_results["errors"].extend(form_validation["errors"])
            elif form_validation["status"] == "warning":
                validation_results["warnings"].extend(form_validation["warnings"])
        
        return validation_results
    
    def _validate_single_form(self, form_name: str, form_data: Dict[str, Any]) -> Dict[str, Any]:
        """Valider un formulaire spécifique"""
        validation = {
            "form_name": form_name,
            "status": "valid",
            "errors": [],
            "warnings": []
        }
        
        # Vérifications communes
        if not form_data.get("company_info", {}).get("name"):
            validation["errors"].append("Nom de l'entreprise manquant")
            validation["status"] = "error"
        
        # Vérifications spécifiques par formulaire
        if "gst" in form_name:
            gst_validation = self._validate_gst_form(form_data)
            validation["errors"].extend(gst_validation["errors"])
            validation["warnings"].extend(gst_validation["warnings"])
            
        elif "qst" in form_name:
            qst_validation = self._validate_qst_form(form_data)
            validation["errors"].extend(qst_validation["errors"])
            validation["warnings"].extend(qst_validation["warnings"])
        
        # Mettre à jour le statut
        if validation["errors"]:
            validation["status"] = "error"
        elif validation["warnings"]:
            validation["status"] = "warning"
        
        return validation
    
    def _validate_gst_form(self, form_data: Dict[str, Any]) -> Dict[str, Any]:
        """Valider le formulaire TPS"""
        validation = {"errors": [], "warnings": []}
        
        fields = form_data.get("fields", {})
        
        if not fields.get("gst_collected") and not fields.get("gst_paid"):
            validation["warnings"].append("Aucune activité TPS détectée")
        
        if fields.get("gst_remittance", 0) < 0:
            validation["warnings"].append("Remise TPS négative - vérifier les calculs")
        
        return validation
    
    def _validate_qst_form(self, form_data: Dict[str, Any]) -> Dict[str, Any]:
        """Valider le formulaire TVQ"""
        validation = {"errors": [], "warnings": []}
        
        fields = form_data.get("fields", {})
        
        if not fields.get("qst_collected") and not fields.get("qst_paid"):
            validation["warnings"].append("Aucune activité TVQ détectée")
        
        if fields.get("qst_remittance", 0) < 0:
            validation["warnings"].append("Remise TVQ négative - vérifier les calculs")
        
        return validation
    
    def prepare_e_filing(self, forms: Dict[str, Any]) -> Dict[str, Any]:
        """Préparer la soumission électronique"""
        e_filing_package = {
            "submission_id": self._generate_submission_id(),
            "submission_date": datetime.now().isoformat(),
            "forms": [],
            "attachments": [],
            "signature": self._generate_digital_signature()
        }
        
        for form_name, form_data in forms.items():
            e_filing_form = {
                "form_name": form_name,
                "form_data": form_data,
                "submission_status": "ready",
                "validation_status": "valid"
            }
            e_filing_package["forms"].append(e_filing_form)
        
        return e_filing_package
    
    def _generate_submission_id(self) -> str:
        """Générer un ID de soumission unique"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"SUBM_{timestamp}_{config.company.name.replace(' ', '_')}"
    
    def _generate_digital_signature(self) -> Dict[str, Any]:
        """Générer une signature électronique"""
        return {
            "signature_type": "digital",
            "signature_date": datetime.now().isoformat(),
            "signer_name": config.company.name,
            "signature_hash": "hash_example"  # À implémenter avec cryptographie
        }
    
    def export_forms(self, forms: Dict[str, Any], format: str = "json") -> str:
        """Exporter les formulaires dans différents formats"""
        if format.lower() == "json":
            return json.dumps(forms, indent=2, default=str)
        elif format.lower() == "pdf":
            return self._generate_pdf_forms(forms)
        elif format.lower() == "xml":
            return self._generate_xml_forms(forms)
        else:
            raise ValueError(f"Format non supporté: {format}")
    
    def _generate_pdf_forms(self, forms: Dict[str, Any]) -> str:
        """Générer les formulaires en PDF"""
        # À implémenter avec une bibliothèque PDF
        return "PDF generation not implemented yet"
    
    def _generate_xml_forms(self, forms: Dict[str, Any]) -> str:
        """Générer les formulaires en XML"""
        # À implémenter avec XML
        return "XML generation not implemented yet"
    
    def get_filing_deadlines(self) -> List[Dict[str, Any]]:
        """Obtenir les échéances de soumission"""
        deadlines = []
        
        # Échéances TPS/TVH trimestrielles
        quarterly_deadlines = self.calendar.get_deadlines_by_type("quarterly")
        for deadline in quarterly_deadlines:
            if "TPS" in deadline.name or "TVH" in deadline.name:
                deadlines.append({
                    "form_type": "gst_qst",
                    "deadline": deadline.date.isoformat(),
                    "description": deadline.description,
                    "priority": deadline.priority
                })
        
        # Échéances annuelles
        annual_deadlines = self.calendar.get_deadlines_by_type("annual")
        for deadline in annual_deadlines:
            if "revenus" in deadline.name:
                deadlines.append({
                    "form_type": "income_tax",
                    "deadline": deadline.date.isoformat(),
                    "description": deadline.description,
                    "priority": deadline.priority
                })
        
        return deadlines
    
    def create_documentation_package(self, forms: Dict[str, Any], 
                                   transactions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Créer un package de documentation complet"""
        package = {
            "package_id": self._generate_submission_id(),
            "creation_date": datetime.now().isoformat(),
            "forms": forms,
            "supporting_documents": [],
            "calculations_summary": {},
            "audit_trail": []
        }
        
        # Ajouter les documents de soutien
        supporting_docs = self._generate_supporting_documents(transactions)
        package["supporting_documents"] = supporting_docs
        
        # Résumé des calculs
        package["calculations_summary"] = self._create_calculations_summary(forms)
        
        # Audit trail
        package["audit_trail"] = self._create_audit_trail(forms)
        
        return package
    
    def _generate_supporting_documents(self, transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Générer les documents de soutien"""
        documents = []
        
        # Résumé des transactions
        documents.append({
            "type": "transaction_summary",
            "name": "Résumé des transactions",
            "content": {
                "total_transactions": len(transactions),
                "total_revenue": sum(t.get('amount', 0) for t in transactions if t.get('type') == 'revenue'),
                "total_expenses": sum(t.get('amount', 0) for t in transactions if t.get('type') == 'expense')
            }
        })
        
        # Justificatifs de dépenses
        expense_docs = [t for t in transactions if t.get('type') == 'expense']
        if expense_docs:
            documents.append({
                "type": "expense_justification",
                "name": "Justificatifs de dépenses",
                "count": len(expense_docs),
                "total_amount": sum(d.get('amount', 0) for d in expense_docs)
            })
        
        return documents
    
    def _create_calculations_summary(self, forms: Dict[str, Any]) -> Dict[str, Any]:
        """Créer un résumé des calculs"""
        summary = {
            "total_tax_obligations": 0,
            "total_deductions": 0,
            "total_credits": 0,
            "net_tax_liability": 0
        }
        
        for form_name, form_data in forms.items():
            if "gst" in form_name or "qst" in form_name:
                fields = form_data.get("fields", {})
                summary["total_tax_obligations"] += fields.get("gst_remittance", 0) + fields.get("qst_remittance", 0)
        
        summary["net_tax_liability"] = summary["total_tax_obligations"] - summary["total_credits"]
        
        return summary
    
    def _create_audit_trail(self, forms: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Créer un audit trail"""
        audit_trail = []
        
        for form_name, form_data in forms.items():
            audit_entry = {
                "timestamp": datetime.now().isoformat(),
                "action": "form_generated",
                "form_name": form_name,
                "form_type": form_data.get("form_type", "unknown"),
                "user": "system"
            }
            audit_trail.append(audit_entry)
        
        return audit_trail 
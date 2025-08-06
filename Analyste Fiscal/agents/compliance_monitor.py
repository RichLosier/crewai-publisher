"""
Agent Moniteur de Conformité - Gardien de la conformité fiscale en temps réel
"""
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from crewai import Agent
from config.settings import config
from config.fiscal_calendar import fiscal_calendar
from config.tax_rules import tax_rules_engine

class ComplianceMonitorAgent:
    """Agent spécialisé dans la surveillance de conformité fiscale en temps réel"""
    
    def __init__(self):
        self.agent = Agent(
            role="Gardien de la conformité fiscale en temps réel",
            goal="Surveiller continuellement la conformité et alerter sur les échéances avec une précision de 100%",
            backstory="""Vous êtes un expert en conformité fiscale avec plus de 12 ans d'expérience 
            dans la surveillance réglementaire. Vous maîtrisez parfaitement les exigences de Revenu Québec, 
            l'ARC, et toutes les réglementations fiscales québécoises et canadiennes. Votre mission est 
            de surveiller en continu la conformité et d'alerter proactivement sur tous les risques et échéances.""",
            verbose=True,
            allow_delegation=False
        )
        
        # Initialiser les outils de surveillance
        self.calendar = fiscal_calendar
        self.tax_engine = tax_rules_engine
        
        # État de surveillance
        self.monitoring_active = True
        self.last_check = None
        self.compliance_status = "compliant"
        self.active_alerts = []
    
    def start_monitoring(self):
        """Démarrer la surveillance continue"""
        self.monitoring_active = True
        self._run_compliance_check()
    
    def stop_monitoring(self):
        """Arrêter la surveillance"""
        self.monitoring_active = False
    
    def run_compliance_check(self, transactions: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Effectuer une vérification complète de conformité"""
        try:
            self.last_check = datetime.now()
            
            compliance_report = {
                "check_time": self.last_check.isoformat(),
                "overall_status": "compliant",
                "deadlines": [],
                "risks": [],
                "violations": [],
                "recommendations": [],
                "alerts": []
            }
            
            # Vérifier les échéances
            deadline_check = self._check_deadlines()
            compliance_report["deadlines"] = deadline_check
            
            # Vérifier les risques de conformité
            risk_check = self._check_compliance_risks(transactions)
            compliance_report["risks"] = risk_check
            
            # Vérifier les violations
            violation_check = self._check_violations(transactions)
            compliance_report["violations"] = violation_check
            
            # Générer les recommandations
            recommendations = self._generate_compliance_recommendations(compliance_report)
            compliance_report["recommendations"] = recommendations
            
            # Générer les alertes
            alerts = self._generate_alerts(compliance_report)
            compliance_report["alerts"] = alerts
            
            # Déterminer le statut global
            if violation_check or any(risk["severity"] == "high" for risk in risk_check):
                compliance_report["overall_status"] = "non_compliant"
            elif any(risk["severity"] == "medium" for risk in risk_check):
                compliance_report["overall_status"] = "at_risk"
            
            self.compliance_status = compliance_report["overall_status"]
            self.active_alerts = alerts
            
            return compliance_report
            
        except Exception as e:
            return {
                "check_time": datetime.now().isoformat(),
                "overall_status": "error",
                "error": str(e),
                "deadlines": [],
                "risks": [],
                "violations": [],
                "recommendations": [],
                "alerts": []
            }
    
    def _check_deadlines(self) -> List[Dict[str, Any]]:
        """Vérifier les échéances fiscales"""
        deadlines = []
        
        # Échéances à venir
        upcoming_deadlines = self.calendar.get_upcoming_deadlines(30)
        for deadline in upcoming_deadlines:
            days_until = (deadline.date - datetime.now()).days
            
            deadline_info = {
                "name": deadline.name,
                "date": deadline.date.isoformat(),
                "description": deadline.description,
                "type": deadline.type,
                "jurisdiction": deadline.jurisdiction,
                "priority": deadline.priority,
                "days_until": days_until,
                "status": "upcoming"
            }
            
            # Déterminer la priorité de l'alerte
            if days_until <= 7:
                deadline_info["alert_level"] = "critical"
            elif days_until <= 14:
                deadline_info["alert_level"] = "high"
            elif days_until <= 21:
                deadline_info["alert_level"] = "medium"
            else:
                deadline_info["alert_level"] = "low"
            
            deadlines.append(deadline_info)
        
        # Échéances en retard
        overdue_deadlines = self.calendar.get_overdue_deadlines()
        for deadline in overdue_deadlines:
            days_overdue = (datetime.now() - deadline.date).days
            
            deadline_info = {
                "name": deadline.name,
                "date": deadline.date.isoformat(),
                "description": deadline.description,
                "type": deadline.type,
                "jurisdiction": deadline.jurisdiction,
                "priority": deadline.priority,
                "days_overdue": days_overdue,
                "status": "overdue",
                "alert_level": "critical"
            }
            
            deadlines.append(deadline_info)
        
        return deadlines
    
    def _check_compliance_risks(self, transactions: List[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Vérifier les risques de conformité"""
        risks = []
        
        # Risques basés sur les seuils
        if transactions:
            total_revenue = sum(t.get('amount', 0) for t in transactions if t.get('type') == 'revenue')
            
            # Seuil d'inscription TPS/TVH
            gst_threshold = 30000
            if total_revenue > gst_threshold:
                risks.append({
                    "type": "registration_threshold",
                    "description": f"Revenus ({total_revenue}) dépassent le seuil d'inscription TPS/TVH ({gst_threshold})",
                    "severity": "high",
                    "action_required": "Inscription immédiate requise"
                })
        
        # Risques basés sur les règles fiscales
        active_rules = self.tax_engine.get_active_rules()
        for rule in active_rules:
            if rule.category == "threshold":
                # Vérifier les seuils critiques
                if rule.name == "QST_Registration_Threshold":
                    if transactions:
                        total_revenue = sum(t.get('amount', 0) for t in transactions if t.get('type') == 'revenue')
                        if total_revenue > rule.value:
                            risks.append({
                                "type": "qst_threshold",
                                "description": f"Seuil TVQ dépassé: {total_revenue} > {rule.value}",
                                "severity": "high",
                                "action_required": "Inscription TVQ requise"
                            })
        
        # Risques de documentation
        if transactions:
            undocumented_transactions = [t for t in transactions if not t.get('documentation')]
            if undocumented_transactions:
                risks.append({
                    "type": "documentation",
                    "description": f"{len(undocumented_transactions)} transactions sans documentation",
                    "severity": "medium",
                    "action_required": "Documentation requise pour audit"
                })
        
        return risks
    
    def _check_violations(self, transactions: List[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Vérifier les violations de conformité"""
        violations = []
        
        if not transactions:
            return violations
        
        # Vérifier les transactions suspectes
        for transaction in transactions:
            amount = transaction.get('amount', 0)
            transaction_type = transaction.get('type', '')
            
            # Transactions négatives suspectes
            if amount < 0 and transaction_type == 'revenue':
                violations.append({
                    "type": "negative_revenue",
                    "description": f"Revenu négatif détecté: {amount}",
                    "transaction_id": transaction.get('id'),
                    "severity": "high",
                    "action_required": "Vérification immédiate requise"
                })
            
            # Montants anormalement élevés
            if amount > 10000:
                violations.append({
                    "type": "high_amount",
                    "description": f"Transaction élevée: {amount}",
                    "transaction_id": transaction.get('id'),
                    "severity": "medium",
                    "action_required": "Documentation supplémentaire requise"
                })
        
        return violations
    
    def _generate_compliance_recommendations(self, compliance_report: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Générer des recommandations de conformité"""
        recommendations = []
        
        # Recommandations basées sur les échéances
        critical_deadlines = [d for d in compliance_report["deadlines"] if d.get("alert_level") == "critical"]
        if critical_deadlines:
            recommendations.append({
                "type": "deadline_priority",
                "description": f"Traiter en priorité {len(critical_deadlines)} échéances critiques",
                "priority": "high",
                "deadlines": [d["name"] for d in critical_deadlines]
            })
        
        # Recommandations basées sur les risques
        high_risks = [r for r in compliance_report["risks"] if r["severity"] == "high"]
        if high_risks:
            recommendations.append({
                "type": "risk_mitigation",
                "description": f"Atténuer {len(high_risks)} risques élevés",
                "priority": "high",
                "risks": [r["type"] for r in high_risks]
            })
        
        # Recommandations générales
        if compliance_report["overall_status"] == "compliant":
            recommendations.append({
                "type": "maintenance",
                "description": "Maintenir les bonnes pratiques de conformité",
                "priority": "low"
            })
        
        return recommendations
    
    def _generate_alerts(self, compliance_report: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Générer des alertes basées sur le rapport de conformité"""
        alerts = []
        
        # Alertes critiques
        critical_deadlines = [d for d in compliance_report["deadlines"] if d.get("alert_level") == "critical"]
        for deadline in critical_deadlines:
            alerts.append({
                "type": "critical_deadline",
                "title": f"Échéance critique: {deadline['name']}",
                "message": f"Échéance dans {deadline.get('days_until', deadline.get('days_overdue', 0))} jours",
                "severity": "critical",
                "action_required": True
            })
        
        # Alertes de risques
        high_risks = [r for r in compliance_report["risks"] if r["severity"] == "high"]
        for risk in high_risks:
            alerts.append({
                "type": "high_risk",
                "title": f"Risque élevé: {risk['type']}",
                "message": risk["description"],
                "severity": "high",
                "action_required": True
            })
        
        # Alertes de violations
        violations = compliance_report["violations"]
        for violation in violations:
            alerts.append({
                "type": "violation",
                "title": f"Violation détectée: {violation['type']}",
                "message": violation["description"],
                "severity": violation["severity"],
                "action_required": True
            })
        
        return alerts
    
    def get_compliance_summary(self) -> Dict[str, Any]:
        """Obtenir un résumé de la conformité"""
        return {
            "status": self.compliance_status,
            "last_check": self.last_check.isoformat() if self.last_check else None,
            "active_alerts_count": len(self.active_alerts),
            "monitoring_active": self.monitoring_active,
            "next_deadline": self._get_next_deadline_info()
        }
    
    def _get_next_deadline_info(self) -> Optional[Dict[str, Any]]:
        """Obtenir les informations sur la prochaine échéance"""
        next_deadline = self.calendar.get_next_deadline()
        if next_deadline:
            days_until = (next_deadline.date - datetime.now()).days
            return {
                "name": next_deadline.name,
                "date": next_deadline.date.isoformat(),
                "days_until": days_until,
                "priority": next_deadline.priority
            }
        return None
    
    def get_regulatory_updates(self) -> List[Dict[str, Any]]:
        """Obtenir les mises à jour réglementaires"""
        # À implémenter avec une API de mises à jour réglementaires
        return [
            {
                "type": "regulatory_update",
                "title": "Mise à jour des taux de TVQ",
                "description": "Nouveaux taux applicables à partir de 2024",
                "effective_date": "2024-01-01",
                "impact": "medium"
            }
        ]
    
    def prepare_audit_documentation(self, period: str = "current_year") -> Dict[str, Any]:
        """Préparer la documentation pour audit"""
        audit_docs = {
            "period": period,
            "preparation_date": datetime.now().isoformat(),
            "required_documents": [],
            "compliance_checklist": [],
            "risk_assessment": {},
            "recommendations": []
        }
        
        # Documents requis
        audit_docs["required_documents"] = [
            "Déclarations TPS/TVH",
            "Déclarations de revenus",
            "Registres comptables",
            "Justificatifs de dépenses",
            "Calculs de déductions"
        ]
        
        # Checklist de conformité
        audit_docs["compliance_checklist"] = [
            "Toutes les échéances respectées",
            "Documentation complète",
            "Calculs fiscaux précis",
            "Déductions justifiées",
            "Crédits d'impôt éligibles"
        ]
        
        return audit_docs
    
    def monitor_real_time(self, interval_minutes: int = 30):
        """Surveillance en temps réel"""
        import schedule
        import time
        
        def check_compliance():
            if self.monitoring_active:
                self.run_compliance_check()
        
        # Programmer la vérification périodique
        schedule.every(interval_minutes).minutes.do(check_compliance)
        
        while self.monitoring_active:
            schedule.run_pending()
            time.sleep(60)  # Vérifier toutes les minutes
    
    def get_compliance_score(self) -> Dict[str, Any]:
        """Calculer un score de conformité"""
        if not self.last_check:
            return {"score": 0, "status": "no_data"}
        
        # Logique de calcul du score basée sur les violations et risques
        # À implémenter selon les besoins spécifiques
        return {
            "score": 85,  # Score exemple
            "status": "good",
            "factors": {
                "deadlines": 90,
                "documentation": 80,
                "calculations": 95,
                "risk_management": 85
            }
        } 
"""
Agent Collecteur de Données - Expert en collecte et synchronisation de données financières multi-plateformes
"""
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import pandas as pd
from crewai import Agent
from config.settings import config
from tools.xero_integration import XeroDataExtractor
from tools.stripe_integration import StripeDataSyncer
from tools.desjardins_integration import BankDataParser
from tools.ai_learning_tools import DataValidator

class DataCollectorAgent:
    """Agent spécialisé dans la collecte et synchronisation de données financières"""
    
    def __init__(self):
        self.agent = Agent(
            role="Expert en collecte et synchronisation de données financières multi-plateformes",
            goal="Collecter automatiquement toutes les données financières depuis Xero, Stripe, et autres sources avec une précision de 99.9%",
            backstory="""Vous êtes un expert en intégration de données financières avec plus de 10 ans d'expérience 
            dans la synchronisation de systèmes comptables. Vous avez une expertise approfondie dans l'extraction 
            de données depuis Xero, Stripe, et les banques québécoises. Votre mission est d'assurer une collecte 
            complète et précise de toutes les données financières nécessaires pour l'analyse fiscale.""",
            verbose=True,
            allow_delegation=False
        )
        
        # Initialiser les outils d'intégration
        self.xero_extractor = XeroDataExtractor()
        self.stripe_syncer = StripeDataSyncer()
        self.bank_parser = BankDataParser()
        self.data_validator = DataValidator()
        
        # État de synchronisation
        self.last_sync_time = None
        self.sync_status = "idle"
        self.data_cache = {}
    
    def collect_all_data(self, force_refresh: bool = False) -> Dict[str, Any]:
        """Collecter toutes les données financières depuis toutes les sources"""
        try:
            self.sync_status = "collecting"
            
            collected_data = {
                "xero_data": {},
                "stripe_data": {},
                "bank_data": {},
                "metadata": {
                    "collection_time": datetime.now().isoformat(),
                    "force_refresh": force_refresh,
                    "sources": []
                }
            }
            
            # Collecter depuis Xero
            if config.api.xero_client_id and config.api.xero_client_secret:
                try:
                    xero_data = self.xero_extractor.extract_all_data(force_refresh)
                    collected_data["xero_data"] = xero_data
                    collected_data["metadata"]["sources"].append("xero")
                except Exception as e:
                    print(f"Erreur lors de la collecte Xero: {e}")
            
            # Collecter depuis Stripe
            if config.api.stripe_secret_key:
                try:
                    stripe_data = self.stripe_syncer.sync_all_data(force_refresh)
                    collected_data["stripe_data"] = stripe_data
                    collected_data["metadata"]["sources"].append("stripe")
                except Exception as e:
                    print(f"Erreur lors de la collecte Stripe: {e}")
            
            # Collecter depuis les banques
            try:
                bank_data = self.bank_parser.parse_all_statements()
                collected_data["bank_data"] = bank_data
                collected_data["metadata"]["sources"].append("bank")
            except Exception as e:
                print(f"Erreur lors de la collecte bancaire: {e}")
            
            # Valider et nettoyer les données
            validated_data = self.data_validator.validate_and_clean(collected_data)
            
            # Mettre en cache
            self.data_cache = validated_data
            self.last_sync_time = datetime.now()
            self.sync_status = "completed"
            
            return validated_data
            
        except Exception as e:
            self.sync_status = "error"
            raise Exception(f"Erreur lors de la collecte de données: {e}")
    
    def get_transactions(self, start_date: Optional[datetime] = None, 
                        end_date: Optional[datetime] = None) -> List[Dict[str, Any]]:
        """Obtenir toutes les transactions pour une période donnée"""
        if not self.data_cache or self._should_refresh_cache():
            self.collect_all_data()
        
        all_transactions = []
        
        # Extraire les transactions Xero
        if "xero_data" in self.data_cache and "transactions" in self.data_cache["xero_data"]:
            all_transactions.extend(self.data_cache["xero_data"]["transactions"])
        
        # Extraire les transactions Stripe
        if "stripe_data" in self.data_cache and "transactions" in self.data_cache["stripe_data"]:
            all_transactions.extend(self.data_cache["stripe_data"]["transactions"])
        
        # Extraire les transactions bancaires
        if "bank_data" in self.data_cache and "transactions" in self.data_cache["bank_data"]:
            all_transactions.extend(self.data_cache["bank_data"]["transactions"])
        
        # Filtrer par date si spécifié
        if start_date or end_date:
            filtered_transactions = []
            for transaction in all_transactions:
                transaction_date = datetime.fromisoformat(transaction.get("date", ""))
                
                if start_date and transaction_date < start_date:
                    continue
                if end_date and transaction_date > end_date:
                    continue
                
                filtered_transactions.append(transaction)
            
            return filtered_transactions
        
        return all_transactions
    
    def get_revenue_breakdown(self, period: str = "current_month") -> Dict[str, Any]:
        """Obtenir la répartition des revenus par source"""
        transactions = self.get_transactions()
        
        revenue_sources = {}
        total_revenue = 0
        
        for transaction in transactions:
            if transaction.get("type") == "revenue":
                amount = float(transaction.get("amount", 0))
                source = transaction.get("source", "unknown")
                
                if source not in revenue_sources:
                    revenue_sources[source] = 0
                
                revenue_sources[source] += amount
                total_revenue += amount
        
        return {
            "total_revenue": total_revenue,
            "revenue_sources": revenue_sources,
            "period": period,
            "collection_time": datetime.now().isoformat()
        }
    
    def get_expense_breakdown(self, period: str = "current_month") -> Dict[str, Any]:
        """Obtenir la répartition des dépenses par catégorie"""
        transactions = self.get_transactions()
        
        expense_categories = {}
        total_expenses = 0
        
        for transaction in transactions:
            if transaction.get("type") == "expense":
                amount = float(transaction.get("amount", 0))
                category = transaction.get("category", "uncategorized")
                
                if category not in expense_categories:
                    expense_categories[category] = 0
                
                expense_categories[category] += amount
                total_expenses += amount
        
        return {
            "total_expenses": total_expenses,
            "expense_categories": expense_categories,
            "period": period,
            "collection_time": datetime.now().isoformat()
        }
    
    def get_tax_relevant_data(self) -> Dict[str, Any]:
        """Extraire les données pertinentes pour l'analyse fiscale"""
        transactions = self.get_transactions()
        
        tax_relevant_data = {
            "gst_collected": 0,
            "gst_paid": 0,
            "qst_collected": 0,
            "qst_paid": 0,
            "taxable_revenue": 0,
            "deductible_expenses": 0,
            "capital_expenses": 0,
            "home_office_expenses": 0,
            "sred_eligible_expenses": 0
        }
        
        for transaction in transactions:
            amount = float(transaction.get("amount", 0))
            transaction_type = transaction.get("type", "")
            category = transaction.get("category", "")
            
            # Taxes collectées
            if transaction_type == "revenue":
                tax_relevant_data["taxable_revenue"] += amount
                gst_amount = float(transaction.get("gst_amount", 0))
                qst_amount = float(transaction.get("qst_amount", 0))
                tax_relevant_data["gst_collected"] += gst_amount
                tax_relevant_data["qst_collected"] += qst_amount
            
            # Taxes payées
            elif transaction_type == "expense":
                gst_amount = float(transaction.get("gst_amount", 0))
                qst_amount = float(transaction.get("qst_amount", 0))
                tax_relevant_data["gst_paid"] += gst_amount
                tax_relevant_data["qst_paid"] += qst_amount
                
                # Catégoriser les dépenses
                if category in ["office_supplies", "utilities", "rent"]:
                    tax_relevant_data["deductible_expenses"] += amount
                elif category in ["equipment", "software", "furniture"]:
                    tax_relevant_data["capital_expenses"] += amount
                elif category == "home_office":
                    tax_relevant_data["home_office_expenses"] += amount
                elif category in ["research", "development", "rd"]:
                    tax_relevant_data["sred_eligible_expenses"] += amount
        
        return tax_relevant_data
    
    def detect_anomalies(self) -> List[Dict[str, Any]]:
        """Détecter les anomalies dans les données collectées"""
        transactions = self.get_transactions()
        anomalies = []
        
        # Détecter les transactions manquantes
        expected_sources = ["xero", "stripe", "bank"]
        collected_sources = set()
        
        for transaction in transactions:
            source = transaction.get("source", "")
            if source:
                collected_sources.add(source)
        
        missing_sources = set(expected_sources) - collected_sources
        if missing_sources:
            anomalies.append({
                "type": "missing_source",
                "description": f"Sources manquantes: {missing_sources}",
                "severity": "high"
            })
        
        # Détecter les montants anormaux
        for transaction in transactions:
            amount = float(transaction.get("amount", 0))
            
            if amount > 10000:  # Montant élevé
                anomalies.append({
                    "type": "high_amount",
                    "description": f"Transaction élevée: ${amount}",
                    "transaction_id": transaction.get("id"),
                    "severity": "medium"
                })
            
            if amount < 0 and transaction.get("type") == "revenue":
                anomalies.append({
                    "type": "negative_revenue",
                    "description": f"Revenu négatif: ${amount}",
                    "transaction_id": transaction.get("id"),
                    "severity": "high"
                })
        
        return anomalies
    
    def get_sync_status(self) -> Dict[str, Any]:
        """Obtenir le statut de synchronisation"""
        return {
            "status": self.sync_status,
            "last_sync_time": self.last_sync_time.isoformat() if self.last_sync_time else None,
            "cache_size": len(self.data_cache) if self.data_cache else 0,
            "sources_available": self._get_available_sources()
        }
    
    def _should_refresh_cache(self) -> bool:
        """Déterminer si le cache doit être rafraîchi"""
        if not self.last_sync_time:
            return True
        
        # Rafraîchir si plus de 1 heure s'est écoulée
        time_since_sync = datetime.now() - self.last_sync_time
        return time_since_sync > timedelta(hours=1)
    
    def _get_available_sources(self) -> List[str]:
        """Obtenir la liste des sources disponibles"""
        sources = []
        
        if config.api.xero_client_id and config.api.xero_client_secret:
            sources.append("xero")
        
        if config.api.stripe_secret_key:
            sources.append("stripe")
        
        # Toujours disponible pour les relevés bancaires
        sources.append("bank")
        
        return sources
    
    def export_data(self, format: str = "json", filepath: Optional[str] = None) -> str:
        """Exporter les données collectées"""
        if not self.data_cache:
            self.collect_all_data()
        
        if format.lower() == "json":
            import json
            data = json.dumps(self.data_cache, indent=2, default=str)
        elif format.lower() == "csv":
            # Convertir en DataFrame pandas puis en CSV
            transactions = self.get_transactions()
            df = pd.DataFrame(transactions)
            data = df.to_csv(index=False)
        else:
            raise ValueError(f"Format non supporté: {format}")
        
        if filepath:
            with open(filepath, 'w') as f:
                f.write(data)
            return filepath
        else:
            return data 
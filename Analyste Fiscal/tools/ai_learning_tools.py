"""
Outils d'Apprentissage AI - Validation et nettoyage des données
"""
from typing import Dict, List, Any, Optional
from datetime import datetime
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

class DataValidator:
    """Validateur et nettoyeur de données pour le système fiscal AI"""
    
    def __init__(self):
        self.validation_rules = self._load_validation_rules()
        self.anomaly_detector = IsolationForest(contamination=0.1, random_state=42)
        self.scaler = StandardScaler()
        self.validation_history = []
    
    def _load_validation_rules(self) -> Dict[str, Any]:
        """Charger les règles de validation"""
        return {
            "amount_limits": {
                "min": -1000000,
                "max": 1000000,
                "required": True
            },
            "date_limits": {
                "min_date": "2020-01-01",
                "max_date": datetime.now().strftime("%Y-%m-%d"),
                "required": True
            },
            "required_fields": [
                "id", "date", "amount", "type", "description", "source"
            ],
            "type_values": ["revenue", "expense", "transfer"],
            "source_values": ["xero", "stripe", "desjardins", "manual"]
        }
    
    def validate_and_clean(self, collected_data: Dict[str, Any]) -> Dict[str, Any]:
        """Valider et nettoyer toutes les données collectées"""
        validation_results = {
            "original_data": collected_data,
            "cleaned_data": {},
            "validation_summary": {},
            "anomalies": [],
            "errors": [],
            "warnings": []
        }
        
        try:
            # Valider la structure des données
            structure_validation = self._validate_data_structure(collected_data)
            validation_results["validation_summary"]["structure"] = structure_validation
            
            # Nettoyer et valider les transactions
            if "transactions" in collected_data:
                cleaned_transactions = self._clean_transactions(collected_data["transactions"])
                validation_results["cleaned_data"]["transactions"] = cleaned_transactions
                
                # Détecter les anomalies
                anomalies = self._detect_anomalies(cleaned_transactions)
                validation_results["anomalies"] = anomalies
            
            # Nettoyer et valider les autres données
            for key, value in collected_data.items():
                if key != "transactions" and key != "metadata":
                    validation_results["cleaned_data"][key] = self._clean_generic_data(value)
            
            # Ajouter les métadonnées de validation
            validation_results["cleaned_data"]["metadata"] = {
                "validation_time": datetime.now().isoformat(),
                "original_count": len(collected_data.get("transactions", [])),
                "cleaned_count": len(validation_results["cleaned_data"].get("transactions", [])),
                "anomalies_count": len(validation_results["anomalies"]),
                "validation_rules_applied": list(self.validation_rules.keys())
            }
            
            # Sauvegarder l'historique
            self.validation_history.append({
                "timestamp": datetime.now().isoformat(),
                "original_count": len(collected_data.get("transactions", [])),
                "cleaned_count": len(validation_results["cleaned_data"].get("transactions", [])),
                "anomalies_count": len(validation_results["anomalies"])
            })
            
            return validation_results["cleaned_data"]
            
        except Exception as e:
            validation_results["errors"].append(f"Erreur lors de la validation: {e}")
            return collected_data
    
    def _validate_data_structure(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Valider la structure des données"""
        validation = {
            "valid": True,
            "missing_sources": [],
            "structure_errors": []
        }
        
        # Vérifier les sources requises
        expected_sources = ["xero", "stripe", "desjardins"]
        found_sources = []
        
        for key, value in data.items():
            if key.endswith("_data") and isinstance(value, dict):
                source = key.replace("_data", "")
                found_sources.append(source)
        
        missing_sources = [s for s in expected_sources if s not in found_sources]
        validation["missing_sources"] = missing_sources
        
        if missing_sources:
            validation["valid"] = False
            validation["structure_errors"].append(f"Sources manquantes: {missing_sources}")
        
        return validation
    
    def _clean_transactions(self, transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Nettoyer et valider les transactions"""
        cleaned_transactions = []
        
        for transaction in transactions:
            cleaned_transaction = self._clean_single_transaction(transaction)
            if cleaned_transaction:
                cleaned_transactions.append(cleaned_transaction)
        
        return cleaned_transactions
    
    def _clean_single_transaction(self, transaction: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Nettoyer une transaction individuelle"""
        try:
            cleaned = transaction.copy()
            
            # Valider et nettoyer l'ID
            if not cleaned.get("id"):
                cleaned["id"] = f"auto_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{len(cleaned_transactions)}"
            
            # Valider et nettoyer la date
            date_str = cleaned.get("date", "")
            if date_str:
                try:
                    if isinstance(date_str, str):
                        date_obj = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                    else:
                        date_obj = date_str
                    
                    # Vérifier les limites de date
                    min_date = datetime.strptime(self.validation_rules["date_limits"]["min_date"], "%Y-%m-%d")
                    max_date = datetime.strptime(self.validation_rules["date_limits"]["max_date"], "%Y-%m-%d")
                    
                    if min_date <= date_obj <= max_date:
                        cleaned["date"] = date_obj.isoformat()
                    else:
                        return None  # Date hors limites
                except:
                    return None  # Date invalide
            
            # Valider et nettoyer le montant
            amount = cleaned.get("amount", 0)
            try:
                amount = float(amount)
                if self.validation_rules["amount_limits"]["min"] <= amount <= self.validation_rules["amount_limits"]["max"]:
                    cleaned["amount"] = amount
                else:
                    return None  # Montant hors limites
            except:
                return None  # Montant invalide
            
            # Valider et nettoyer le type
            transaction_type = cleaned.get("type", "")
            if transaction_type not in self.validation_rules["type_values"]:
                cleaned["type"] = "uncategorized"
            
            # Valider et nettoyer la source
            source = cleaned.get("source", "")
            if source not in self.validation_rules["source_values"]:
                cleaned["source"] = "unknown"
            
            # Nettoyer la description
            description = cleaned.get("description", "")
            if description:
                cleaned["description"] = description.strip()
            else:
                cleaned["description"] = "Transaction sans description"
            
            # Nettoyer la catégorie
            category = cleaned.get("category", "")
            if category:
                cleaned["category"] = category.strip()
            else:
                cleaned["category"] = "uncategorized"
            
            # Nettoyer les montants de taxes
            gst_amount = cleaned.get("gst_amount", 0)
            qst_amount = cleaned.get("qst_amount", 0)
            
            try:
                cleaned["gst_amount"] = float(gst_amount)
                cleaned["qst_amount"] = float(qst_amount)
            except:
                cleaned["gst_amount"] = 0.0
                cleaned["qst_amount"] = 0.0
            
            return cleaned
            
        except Exception as e:
            print(f"Erreur lors du nettoyage de la transaction: {e}")
            return None
    
    def _clean_generic_data(self, data: Any) -> Any:
        """Nettoyer des données génériques"""
        if isinstance(data, list):
            return [item for item in data if item is not None]
        elif isinstance(data, dict):
            return {k: v for k, v in data.items() if v is not None}
        else:
            return data
    
    def _detect_anomalies(self, transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Détecter les anomalies dans les transactions"""
        if not transactions:
            return []
        
        try:
            # Préparer les données pour l'analyse
            df = pd.DataFrame(transactions)
            
            # Sélectionner les caractéristiques numériques
            numeric_features = ['amount', 'gst_amount', 'qst_amount']
            available_features = [f for f in numeric_features if f in df.columns]
            
            if not available_features:
                return []
            
            # Préparer les données
            X = df[available_features].fillna(0)
            
            # Normaliser les données
            X_scaled = self.scaler.fit_transform(X)
            
            # Détecter les anomalies
            anomaly_labels = self.anomaly_detector.fit_predict(X_scaled)
            
            # Identifier les transactions anormales
            anomalies = []
            for i, label in enumerate(anomaly_labels):
                if label == -1:  # Anomalie détectée
                    anomaly_info = {
                        "transaction_id": transactions[i].get("id", f"unknown_{i}"),
                        "anomaly_type": "statistical",
                        "severity": "medium",
                        "features": {
                            feature: transactions[i].get(feature, 0) 
                            for feature in available_features
                        },
                        "description": f"Transaction statistiquement anormale basée sur {available_features}"
                    }
                    anomalies.append(anomaly_info)
            
            return anomalies
            
        except Exception as e:
            print(f"Erreur lors de la détection d'anomalies: {e}")
            return []
    
    def get_validation_summary(self) -> Dict[str, Any]:
        """Obtenir un résumé des validations"""
        if not self.validation_history:
            return {"error": "Aucun historique de validation disponible"}
        
        total_validations = len(self.validation_history)
        total_original = sum(v["original_count"] for v in self.validation_history)
        total_cleaned = sum(v["cleaned_count"] for v in self.validation_history)
        total_anomalies = sum(v["anomalies_count"] for v in self.validation_history)
        
        return {
            "total_validations": total_validations,
            "total_original_transactions": total_original,
            "total_cleaned_transactions": total_cleaned,
            "total_anomalies_detected": total_anomalies,
            "average_cleaning_rate": (total_cleaned / total_original * 100) if total_original > 0 else 0,
            "average_anomaly_rate": (total_anomalies / total_original * 100) if total_original > 0 else 0,
            "last_validation": self.validation_history[-1]["timestamp"] if self.validation_history else None
        }
    
    def get_data_quality_metrics(self, transactions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Obtenir des métriques de qualité des données"""
        if not transactions:
            return {"error": "Aucune transaction disponible"}
        
        df = pd.DataFrame(transactions)
        
        metrics = {
            "total_transactions": len(transactions),
            "completeness": {},
            "consistency": {},
            "accuracy": {}
        }
        
        # Métriques de complétude
        required_fields = self.validation_rules["required_fields"]
        for field in required_fields:
            if field in df.columns:
                completeness = (df[field].notna().sum() / len(df)) * 100
                metrics["completeness"][field] = completeness
            else:
                metrics["completeness"][field] = 0.0
        
        # Métriques de cohérence
        if "type" in df.columns:
            valid_types = self.validation_rules["type_values"]
            consistency = (df["type"].isin(valid_types).sum() / len(df)) * 100
            metrics["consistency"]["type"] = consistency
        
        if "source" in df.columns:
            valid_sources = self.validation_rules["source_values"]
            consistency = (df["source"].isin(valid_sources).sum() / len(df)) * 100
            metrics["consistency"]["source"] = consistency
        
        # Métriques de précision
        if "amount" in df.columns:
            amount_range = self.validation_rules["amount_limits"]
            within_range = ((df["amount"] >= amount_range["min"]) & 
                          (df["amount"] <= amount_range["max"])).sum()
            accuracy = (within_range / len(df)) * 100
            metrics["accuracy"]["amount"] = accuracy
        
        return metrics
    
    def suggest_improvements(self, transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Suggérer des améliorations pour les données"""
        suggestions = []
        
        if not transactions:
            return suggestions
        
        df = pd.DataFrame(transactions)
        
        # Vérifier les champs manquants
        required_fields = self.validation_rules["required_fields"]
        for field in required_fields:
            if field not in df.columns or df[field].isna().sum() > 0:
                suggestions.append({
                    "type": "missing_field",
                    "field": field,
                    "description": f"Champ requis manquant ou incomplet: {field}",
                    "priority": "high"
                })
        
        # Vérifier les types invalides
        if "type" in df.columns:
            invalid_types = df[~df["type"].isin(self.validation_rules["type_values"])]
            if len(invalid_types) > 0:
                suggestions.append({
                    "type": "invalid_values",
                    "field": "type",
                    "description": f"{len(invalid_types)} transactions avec des types invalides",
                    "priority": "medium"
                })
        
        # Vérifier les sources invalides
        if "source" in df.columns:
            invalid_sources = df[~df["source"].isin(self.validation_rules["source_values"])]
            if len(invalid_sources) > 0:
                suggestions.append({
                    "type": "invalid_values",
                    "field": "source",
                    "description": f"{len(invalid_sources)} transactions avec des sources invalides",
                    "priority": "medium"
                })
        
        # Vérifier les montants extrêmes
        if "amount" in df.columns:
            amount_range = self.validation_rules["amount_limits"]
            extreme_amounts = df[(df["amount"] < amount_range["min"]) | 
                               (df["amount"] > amount_range["max"])]
            if len(extreme_amounts) > 0:
                suggestions.append({
                    "type": "extreme_values",
                    "field": "amount",
                    "description": f"{len(extreme_amounts)} transactions avec des montants extrêmes",
                    "priority": "low"
                })
        
        return suggestions
    
    def export_validation_report(self, transactions: List[Dict[str, Any]], 
                               format: str = "json") -> str:
        """Exporter un rapport de validation"""
        report = {
            "validation_timestamp": datetime.now().isoformat(),
            "data_quality_metrics": self.get_data_quality_metrics(transactions),
            "validation_summary": self.get_validation_summary(),
            "improvement_suggestions": self.suggest_improvements(transactions),
            "validation_rules_applied": self.validation_rules
        }
        
        if format.lower() == "json":
            import json
            return json.dumps(report, indent=2, default=str)
        else:
            raise ValueError(f"Format non supporté: {format}") 
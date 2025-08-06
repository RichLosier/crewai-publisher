"""
Intégration Desjardins - Traitement des relevés bancaires
"""
from typing import Dict, List, Any, Optional
from datetime import datetime
import csv
import os
from config.settings import config

class BankDataParser:
    """Parseur de données bancaires pour le système fiscal AI"""
    
    def __init__(self):
        self.api_key = config.api.desjardins_api_key
        self.api_available = self._check_api_availability()
        self.data_cache = {}
        self.last_parse = None
    
    def _check_api_availability(self) -> bool:
        """Vérifier si l'API Desjardins est disponible"""
        # Pour l'instant, on simule que l'API n'est pas disponible
        # et on utilise le traitement de fichiers CSV
        return False
    
    def parse_all_statements(self) -> Dict[str, Any]:
        """Parser tous les relevés bancaires disponibles"""
        try:
            parsed_data = {
                "transactions": [],
                "accounts": [],
                "statements": [],
                "metadata": {
                    "parse_time": datetime.now().isoformat(),
                    "source": "desjardins",
                    "method": "csv_processing"
                }
            }
            
            # Traiter les fichiers CSV disponibles
            csv_transactions = self._parse_csv_statements()
            parsed_data["transactions"] = csv_transactions
            
            # Traiter les comptes
            accounts = self._parse_accounts()
            parsed_data["accounts"] = accounts
            
            # Traiter les relevés
            statements = self._parse_statements()
            parsed_data["statements"] = statements
            
            # Mettre en cache
            self.data_cache = parsed_data
            self.last_parse = datetime.now()
            
            return parsed_data
            
        except Exception as e:
            print(f"Erreur lors du parsing des relevés bancaires: {e}")
            return {"error": str(e)}
    
    def _parse_csv_statements(self) -> List[Dict[str, Any]]:
        """Parser les relevés CSV"""
        transactions = []
        
        # Chercher les fichiers CSV dans le répertoire data
        csv_directory = os.path.join(config.data_path, "bank_statements")
        os.makedirs(csv_directory, exist_ok=True)
        
        csv_files = [f for f in os.listdir(csv_directory) if f.endswith('.csv')]
        
        for csv_file in csv_files:
            file_path = os.path.join(csv_directory, csv_file)
            file_transactions = self._parse_single_csv(file_path)
            transactions.extend(file_transactions)
        
        return transactions
    
    def _parse_single_csv(self, file_path: str) -> List[Dict[str, Any]]:
        """Parser un fichier CSV individuel"""
        transactions = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                for row in reader:
                    transaction = self._convert_csv_row_to_transaction(row)
                    if transaction:
                        transactions.append(transaction)
        
        except Exception as e:
            print(f"Erreur lors du parsing du fichier {file_path}: {e}")
        
        return transactions
    
    def _convert_csv_row_to_transaction(self, row: Dict[str, str]) -> Optional[Dict[str, Any]]:
        """Convertir une ligne CSV en transaction standard"""
        try:
            # Essayer différents formats de date
            date_str = row.get('Date', row.get('DATE', row.get('date', '')))
            date_obj = self._parse_date(date_str)
            
            if not date_obj:
                return None
            
            # Essayer différents formats de montant
            amount_str = row.get('Amount', row.get('AMOUNT', row.get('amount', '0')))
            amount = self._parse_amount(amount_str)
            
            # Déterminer le type de transaction
            transaction_type = self._determine_transaction_type(amount, row)
            
            # Déterminer la catégorie
            category = self._determine_category(row)
            
            return {
                "id": f"bank_{date_obj.strftime('%Y%m%d')}_{len(transactions)}",
                "date": date_obj.isoformat(),
                "amount": amount,
                "type": transaction_type,
                "description": row.get('Description', row.get('DESCRIPTION', row.get('description', ''))),
                "category": category,
                "source": "desjardins",
                "gst_amount": 0,  # À calculer si nécessaire
                "qst_amount": 0,  # À calculer si nécessaire
                "account": row.get('Account', row.get('ACCOUNT', '')),
                "reference": row.get('Reference', row.get('REFERENCE', '')),
                "status": "completed"
            }
        
        except Exception as e:
            print(f"Erreur lors de la conversion de la ligne CSV: {e}")
            return None
    
    def _parse_date(self, date_str: str) -> Optional[datetime]:
        """Parser une date depuis une chaîne"""
        if not date_str:
            return None
        
        # Essayer différents formats de date
        date_formats = [
            "%Y-%m-%d",
            "%d/%m/%Y",
            "%m/%d/%Y",
            "%Y/%m/%d",
            "%d-%m-%Y",
            "%m-%d-%Y"
        ]
        
        for fmt in date_formats:
            try:
                return datetime.strptime(date_str.strip(), fmt)
            except ValueError:
                continue
        
        return None
    
    def _parse_amount(self, amount_str: str) -> float:
        """Parser un montant depuis une chaîne"""
        if not amount_str:
            return 0.0
        
        try:
            # Nettoyer la chaîne
            cleaned = amount_str.strip().replace('$', '').replace(',', '')
            return float(cleaned)
        except ValueError:
            return 0.0
    
    def _determine_transaction_type(self, amount: float, row: Dict[str, str]) -> str:
        """Déterminer le type de transaction"""
        if amount > 0:
            return "revenue"
        elif amount < 0:
            return "expense"
        else:
            return "transfer"
    
    def _determine_category(self, row: Dict[str, str]) -> str:
        """Déterminer la catégorie de transaction"""
        description = row.get('Description', row.get('DESCRIPTION', row.get('description', ''))).lower()
        
        # Mots-clés pour catégorisation
        categories = {
            'office_supplies': ['bureau', 'fournitures', 'papeterie', 'staples'],
            'utilities': ['hydro', 'électricité', 'gaz', 'téléphone', 'internet'],
            'rent': ['loyer', 'rent', 'bail'],
            'marketing': ['publicité', 'marketing', 'ads', 'google'],
            'software': ['logiciel', 'software', 'subscription', 'abonnement'],
            'equipment': ['équipement', 'equipment', 'matériel'],
            'travel': ['voyage', 'travel', 'transport', 'essence'],
            'meals': ['repas', 'restaurant', 'café', 'meals'],
            'insurance': ['assurance', 'insurance'],
            'banking': ['frais bancaires', 'bank fees', 'intérêts']
        }
        
        for category, keywords in categories.items():
            for keyword in keywords:
                if keyword in description:
                    return category
        
        return "uncategorized"
    
    def _parse_accounts(self) -> List[Dict[str, Any]]:
        """Parser les informations de comptes"""
        accounts = []
        
        # Informations de base des comptes (à étendre selon les besoins)
        accounts.append({
            "id": "main_account",
            "name": "Compte principal",
            "type": "checking",
            "source": "desjardins",
            "status": "active"
        })
        
        return accounts
    
    def _parse_statements(self) -> List[Dict[str, Any]]:
        """Parser les relevés de compte"""
        statements = []
        
        # Chercher les fichiers de relevés
        statement_directory = os.path.join(config.data_path, "bank_statements")
        
        if os.path.exists(statement_directory):
            for file in os.listdir(statement_directory):
                if file.endswith(('.pdf', '.csv')):
                    statements.append({
                        "id": file,
                        "name": file,
                        "type": "bank_statement",
                        "source": "desjardins",
                        "file_path": os.path.join(statement_directory, file),
                        "parse_date": datetime.now().isoformat()
                    })
        
        return statements
    
    def get_transaction_summary(self) -> Dict[str, Any]:
        """Obtenir un résumé des transactions bancaires"""
        if not self.data_cache:
            return {"error": "Aucune donnée disponible"}
        
        transactions = self.data_cache.get("transactions", [])
        
        total_revenue = sum(t.get("amount", 0) for t in transactions if t.get("type") == "revenue")
        total_expenses = sum(t.get("amount", 0) for t in transactions if t.get("type") == "expense")
        
        # Analyser par catégorie
        categories = {}
        for transaction in transactions:
            category = transaction.get("category", "uncategorized")
            amount = transaction.get("amount", 0)
            
            if category not in categories:
                categories[category] = 0
            categories[category] += abs(amount)
        
        return {
            "total_transactions": len(transactions),
            "total_revenue": total_revenue,
            "total_expenses": total_expenses,
            "net_flow": total_revenue - total_expenses,
            "categories": categories,
            "last_parse": self.last_parse.isoformat() if self.last_parse else None
        }
    
    def get_sync_status(self) -> Dict[str, Any]:
        """Obtenir le statut de synchronisation"""
        return {
            "api_available": self.api_available,
            "last_parse": self.last_parse.isoformat() if self.last_parse else None,
            "cache_size": len(self.data_cache) if self.data_cache else 0,
            "method": "csv_processing" if not self.api_available else "api"
        }
    
    def add_csv_statement(self, file_path: str) -> bool:
        """Ajouter un fichier CSV de relevé"""
        try:
            # Copier le fichier vers le répertoire de données
            import shutil
            
            destination_dir = os.path.join(config.data_path, "bank_statements")
            os.makedirs(destination_dir, exist_ok=True)
            
            filename = os.path.basename(file_path)
            destination_path = os.path.join(destination_dir, filename)
            
            shutil.copy2(file_path, destination_path)
            
            print(f"Fichier CSV ajouté: {filename}")
            return True
            
        except Exception as e:
            print(f"Erreur lors de l'ajout du fichier CSV: {e}")
            return False
    
    def validate_csv_format(self, file_path: str) -> Dict[str, Any]:
        """Valider le format d'un fichier CSV"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                # Vérifier les colonnes requises
                required_columns = ['Date', 'Amount', 'Description']
                optional_columns = ['Account', 'Reference', 'Category']
                
                headers = reader.fieldnames or []
                
                missing_required = [col for col in required_columns if col not in headers]
                found_optional = [col for col in optional_columns if col in headers]
                
                # Compter les lignes
                row_count = sum(1 for row in reader)
                
                return {
                    "valid": len(missing_required) == 0,
                    "missing_required": missing_required,
                    "found_optional": found_optional,
                    "row_count": row_count,
                    "headers": headers
                }
                
        except Exception as e:
            return {
                "valid": False,
                "error": str(e)
            } 
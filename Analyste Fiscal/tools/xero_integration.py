"""
Intégration Xero - Extraction complète des données comptables
"""
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import requests
from config.settings import config

class XeroDataExtractor:
    """Extracteur de données Xero pour le système fiscal AI"""
    
    def __init__(self):
        self.client_id = config.api.xero_client_id
        self.client_secret = config.api.xero_client_secret
        self.base_url = "https://api.xero.com/api.xro/2.0"
        self.access_token = None
        self.token_expires = None
        
        # Cache des données
        self.data_cache = {}
        self.last_sync = None
    
    def authenticate(self) -> bool:
        """Authentifier avec l'API Xero"""
        try:
            # Logique d'authentification OAuth2
            # À implémenter selon la documentation Xero
            auth_url = "https://identity.xero.com/connect/token"
            
            auth_data = {
                "grant_type": "client_credentials",
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "scope": "offline_access accounting.transactions accounting.contacts"
            }
            
            response = requests.post(auth_url, data=auth_data)
            
            if response.status_code == 200:
                token_data = response.json()
                self.access_token = token_data["access_token"]
                self.token_expires = datetime.now() + timedelta(seconds=token_data["expires_in"])
                return True
            else:
                print(f"Erreur d'authentification Xero: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"Erreur lors de l'authentification Xero: {e}")
            return False
    
    def _get_headers(self) -> Dict[str, str]:
        """Obtenir les en-têtes pour les requêtes API"""
        if not self.access_token or (self.token_expires and datetime.now() > self.token_expires):
            if not self.authenticate():
                raise Exception("Impossible d'authentifier avec Xero")
        
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
    
    def extract_all_data(self, force_refresh: bool = False) -> Dict[str, Any]:
        """Extraire toutes les données pertinentes depuis Xero"""
        if not force_refresh and self.data_cache and self.last_sync:
            # Vérifier si le cache est encore valide (moins de 1 heure)
            if datetime.now() - self.last_sync < timedelta(hours=1):
                return self.data_cache
        
        try:
            extracted_data = {
                "transactions": [],
                "invoices": [],
                "contacts": [],
                "accounts": [],
                "tax_rates": [],
                "metadata": {
                    "extraction_time": datetime.now().isoformat(),
                    "force_refresh": force_refresh,
                    "source": "xero"
                }
            }
            
            # Extraire les transactions
            transactions = self._extract_transactions()
            extracted_data["transactions"] = transactions
            
            # Extraire les factures
            invoices = self._extract_invoices()
            extracted_data["invoices"] = invoices
            
            # Extraire les contacts
            contacts = self._extract_contacts()
            extracted_data["contacts"] = contacts
            
            # Extraire les comptes
            accounts = self._extract_accounts()
            extracted_data["accounts"] = accounts
            
            # Extraire les taux de taxes
            tax_rates = self._extract_tax_rates()
            extracted_data["tax_rates"] = tax_rates
            
            # Mettre en cache
            self.data_cache = extracted_data
            self.last_sync = datetime.now()
            
            return extracted_data
            
        except Exception as e:
            print(f"Erreur lors de l'extraction des données Xero: {e}")
            return {"error": str(e)}
    
    def _extract_transactions(self) -> List[Dict[str, Any]]:
        """Extraire les transactions depuis Xero"""
        try:
            url = f"{self.base_url}/BankTransactions"
            headers = self._get_headers()
            
            # Paramètres pour obtenir les transactions récentes
            params = {
                "where": "Date >= DateTime(2024, 1, 1)",  # Depuis le début de l'année
                "order": "Date DESC"
            }
            
            response = requests.get(url, headers=headers, params=params)
            
            if response.status_code == 200:
                data = response.json()
                transactions = []
                
                for transaction in data.get("BankTransactions", []):
                    # Convertir au format standard
                    converted_transaction = self._convert_transaction_format(transaction)
                    transactions.append(converted_transaction)
                
                return transactions
            else:
                print(f"Erreur lors de l'extraction des transactions: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"Erreur lors de l'extraction des transactions: {e}")
            return []
    
    def _extract_invoices(self) -> List[Dict[str, Any]]:
        """Extraire les factures depuis Xero"""
        try:
            url = f"{self.base_url}/Invoices"
            headers = self._get_headers()
            
            params = {
                "where": "Date >= DateTime(2024, 1, 1)",
                "order": "Date DESC"
            }
            
            response = requests.get(url, headers=headers, params=params)
            
            if response.status_code == 200:
                data = response.json()
                invoices = []
                
                for invoice in data.get("Invoices", []):
                    # Convertir au format standard
                    converted_invoice = self._convert_invoice_format(invoice)
                    invoices.append(converted_invoice)
                
                return invoices
            else:
                print(f"Erreur lors de l'extraction des factures: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"Erreur lors de l'extraction des factures: {e}")
            return []
    
    def _extract_contacts(self) -> List[Dict[str, Any]]:
        """Extraire les contacts depuis Xero"""
        try:
            url = f"{self.base_url}/Contacts"
            headers = self._get_headers()
            
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                contacts = []
                
                for contact in data.get("Contacts", []):
                    # Convertir au format standard
                    converted_contact = self._convert_contact_format(contact)
                    contacts.append(converted_contact)
                
                return contacts
            else:
                print(f"Erreur lors de l'extraction des contacts: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"Erreur lors de l'extraction des contacts: {e}")
            return []
    
    def _extract_accounts(self) -> List[Dict[str, Any]]:
        """Extraire les comptes depuis Xero"""
        try:
            url = f"{self.base_url}/Accounts"
            headers = self._get_headers()
            
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                accounts = []
                
                for account in data.get("Accounts", []):
                    # Convertir au format standard
                    converted_account = self._convert_account_format(account)
                    accounts.append(converted_account)
                
                return accounts
            else:
                print(f"Erreur lors de l'extraction des comptes: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"Erreur lors de l'extraction des comptes: {e}")
            return []
    
    def _extract_tax_rates(self) -> List[Dict[str, Any]]:
        """Extraire les taux de taxes depuis Xero"""
        try:
            url = f"{self.base_url}/TaxRates"
            headers = self._get_headers()
            
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                tax_rates = []
                
                for tax_rate in data.get("TaxRates", []):
                    # Convertir au format standard
                    converted_tax_rate = self._convert_tax_rate_format(tax_rate)
                    tax_rates.append(converted_tax_rate)
                
                return tax_rates
            else:
                print(f"Erreur lors de l'extraction des taux de taxes: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"Erreur lors de l'extraction des taux de taxes: {e}")
            return []
    
    def _convert_transaction_format(self, xero_transaction: Dict[str, Any]) -> Dict[str, Any]:
        """Convertir une transaction Xero au format standard"""
        return {
            "id": xero_transaction.get("BankTransactionID"),
            "date": xero_transaction.get("Date"),
            "amount": float(xero_transaction.get("Total", 0)),
            "type": self._determine_transaction_type(xero_transaction),
            "description": xero_transaction.get("Reference", ""),
            "category": xero_transaction.get("LineItems", [{}])[0].get("AccountCode", "uncategorized"),
            "source": "xero",
            "gst_amount": self._extract_tax_amount(xero_transaction, "GST"),
            "qst_amount": self._extract_tax_amount(xero_transaction, "QST"),
            "contact_name": xero_transaction.get("Contact", {}).get("Name", ""),
            "status": xero_transaction.get("Status", "unknown")
        }
    
    def _convert_invoice_format(self, xero_invoice: Dict[str, Any]) -> Dict[str, Any]:
        """Convertir une facture Xero au format standard"""
        return {
            "id": xero_invoice.get("InvoiceID"),
            "date": xero_invoice.get("Date"),
            "amount": float(xero_invoice.get("Total", 0)),
            "type": "revenue",
            "description": xero_invoice.get("Reference", ""),
            "category": "sales",
            "source": "xero",
            "gst_amount": self._extract_tax_amount(xero_invoice, "GST"),
            "qst_amount": self._extract_tax_amount(xero_invoice, "QST"),
            "contact_name": xero_invoice.get("Contact", {}).get("Name", ""),
            "status": xero_invoice.get("Status", "unknown"),
            "due_date": xero_invoice.get("DueDate")
        }
    
    def _convert_contact_format(self, xero_contact: Dict[str, Any]) -> Dict[str, Any]:
        """Convertir un contact Xero au format standard"""
        return {
            "id": xero_contact.get("ContactID"),
            "name": xero_contact.get("Name", ""),
            "email": xero_contact.get("EmailAddress", ""),
            "phone": xero_contact.get("Phones", [{}])[0].get("PhoneNumber", ""),
            "type": xero_contact.get("ContactStatus", "unknown"),
            "source": "xero"
        }
    
    def _convert_account_format(self, xero_account: Dict[str, Any]) -> Dict[str, Any]:
        """Convertir un compte Xero au format standard"""
        return {
            "id": xero_account.get("AccountID"),
            "code": xero_account.get("Code", ""),
            "name": xero_account.get("Name", ""),
            "type": xero_account.get("Type", ""),
            "status": xero_account.get("Status", ""),
            "source": "xero"
        }
    
    def _convert_tax_rate_format(self, xero_tax_rate: Dict[str, Any]) -> Dict[str, Any]:
        """Convertir un taux de taxe Xero au format standard"""
        return {
            "id": xero_tax_rate.get("TaxType"),
            "name": xero_tax_rate.get("Name", ""),
            "rate": float(xero_tax_rate.get("EffectiveRate", 0)),
            "type": xero_tax_rate.get("TaxType", ""),
            "status": xero_tax_rate.get("Status", ""),
            "source": "xero"
        }
    
    def _determine_transaction_type(self, transaction: Dict[str, Any]) -> str:
        """Déterminer le type de transaction"""
        amount = float(transaction.get("Total", 0))
        
        if amount > 0:
            return "revenue"
        elif amount < 0:
            return "expense"
        else:
            return "transfer"
    
    def _extract_tax_amount(self, item: Dict[str, Any], tax_type: str) -> float:
        """Extraire le montant de taxe spécifique"""
        try:
            line_items = item.get("LineItems", [])
            total_tax = 0
            
            for line_item in line_items:
                tax_details = line_item.get("TaxType", "")
                if tax_type in tax_details:
                    tax_amount = float(line_item.get("TaxAmount", 0))
                    total_tax += tax_amount
            
            return total_tax
        except:
            return 0.0
    
    def get_transaction_summary(self) -> Dict[str, Any]:
        """Obtenir un résumé des transactions"""
        if not self.data_cache:
            return {"error": "Aucune donnée disponible"}
        
        transactions = self.data_cache.get("transactions", [])
        
        total_revenue = sum(t.get("amount", 0) for t in transactions if t.get("type") == "revenue")
        total_expenses = sum(t.get("amount", 0) for t in transactions if t.get("type") == "expense")
        total_gst = sum(t.get("gst_amount", 0) for t in transactions)
        total_qst = sum(t.get("qst_amount", 0) for t in transactions)
        
        return {
            "total_transactions": len(transactions),
            "total_revenue": total_revenue,
            "total_expenses": total_expenses,
            "net_income": total_revenue - total_expenses,
            "total_gst": total_gst,
            "total_qst": total_qst,
            "last_sync": self.last_sync.isoformat() if self.last_sync else None
        }
    
    def get_sync_status(self) -> Dict[str, Any]:
        """Obtenir le statut de synchronisation"""
        return {
            "authenticated": self.access_token is not None,
            "last_sync": self.last_sync.isoformat() if self.last_sync else None,
            "cache_size": len(self.data_cache) if self.data_cache else 0,
            "token_expires": self.token_expires.isoformat() if self.token_expires else None
        } 
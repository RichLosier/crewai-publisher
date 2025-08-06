"""
Intégration Stripe - Synchronisation des paiements et revenus
"""
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import stripe
from config.settings import config

class StripeDataSyncer:
    """Synchroniseur de données Stripe pour le système fiscal AI"""
    
    def __init__(self):
        self.api_key = config.api.stripe_secret_key
        self.stripe_client = None
        self.data_cache = {}
        self.last_sync = None
        
        if self.api_key:
            stripe.api_key = self.api_key
            self.stripe_client = stripe
    
    def sync_all_data(self, force_refresh: bool = False) -> Dict[str, Any]:
        """Synchroniser toutes les données Stripe"""
        if not self.stripe_client:
            return {"error": "Stripe non configuré"}
        
        if not force_refresh and self.data_cache and self.last_sync:
            # Vérifier si le cache est encore valide (moins de 1 heure)
            if datetime.now() - self.last_sync < timedelta(hours=1):
                return self.data_cache
        
        try:
            synced_data = {
                "transactions": [],
                "payments": [],
                "subscriptions": [],
                "customers": [],
                "fees": [],
                "metadata": {
                    "sync_time": datetime.now().isoformat(),
                    "force_refresh": force_refresh,
                    "source": "stripe"
                }
            }
            
            # Synchroniser les paiements
            payments = self._sync_payments()
            synced_data["payments"] = payments
            
            # Synchroniser les abonnements
            subscriptions = self._sync_subscriptions()
            synced_data["subscriptions"] = subscriptions
            
            # Synchroniser les clients
            customers = self._sync_customers()
            synced_data["customers"] = customers
            
            # Synchroniser les frais
            fees = self._sync_fees()
            synced_data["fees"] = fees
            
            # Convertir en transactions standard
            transactions = self._convert_to_transactions(synced_data)
            synced_data["transactions"] = transactions
            
            # Mettre en cache
            self.data_cache = synced_data
            self.last_sync = datetime.now()
            
            return synced_data
            
        except Exception as e:
            print(f"Erreur lors de la synchronisation Stripe: {e}")
            return {"error": str(e)}
    
    def _sync_payments(self) -> List[Dict[str, Any]]:
        """Synchroniser les paiements Stripe"""
        try:
            payments = []
            
            # Récupérer les paiements des 12 derniers mois
            start_date = datetime.now() - timedelta(days=365)
            
            payment_intents = self.stripe_client.PaymentIntent.list(
                created={'gte': int(start_date.timestamp())},
                limit=100
            )
            
            for payment in payment_intents.data:
                converted_payment = self._convert_payment_format(payment)
                payments.append(converted_payment)
            
            return payments
            
        except Exception as e:
            print(f"Erreur lors de la synchronisation des paiements: {e}")
            return []
    
    def _sync_subscriptions(self) -> List[Dict[str, Any]]:
        """Synchroniser les abonnements Stripe"""
        try:
            subscriptions = []
            
            # Récupérer les abonnements actifs
            subscription_list = self.stripe_client.Subscription.list(
                status='active',
                limit=100
            )
            
            for subscription in subscription_list.data:
                converted_subscription = self._convert_subscription_format(subscription)
                subscriptions.append(converted_subscription)
            
            return subscriptions
            
        except Exception as e:
            print(f"Erreur lors de la synchronisation des abonnements: {e}")
            return []
    
    def _sync_customers(self) -> List[Dict[str, Any]]:
        """Synchroniser les clients Stripe"""
        try:
            customers = []
            
            # Récupérer les clients récents
            customer_list = self.stripe_client.Customer.list(limit=100)
            
            for customer in customer_list.data:
                converted_customer = self._convert_customer_format(customer)
                customers.append(converted_customer)
            
            return customers
            
        except Exception as e:
            print(f"Erreur lors de la synchronisation des clients: {e}")
            return []
    
    def _sync_fees(self) -> List[Dict[str, Any]]:
        """Synchroniser les frais Stripe"""
        try:
            fees = []
            
            # Récupérer les frais des 12 derniers mois
            start_date = datetime.now() - timedelta(days=365)
            
            fee_list = self.stripe_client.ApplicationFee.list(
                created={'gte': int(start_date.timestamp())},
                limit=100
            )
            
            for fee in fee_list.data:
                converted_fee = self._convert_fee_format(fee)
                fees.append(converted_fee)
            
            return fees
            
        except Exception as e:
            print(f"Erreur lors de la synchronisation des frais: {e}")
            return []
    
    def _convert_payment_format(self, stripe_payment: Any) -> Dict[str, Any]:
        """Convertir un paiement Stripe au format standard"""
        return {
            "id": stripe_payment.id,
            "date": datetime.fromtimestamp(stripe_payment.created).isoformat(),
            "amount": float(stripe_payment.amount) / 100,  # Convertir en dollars
            "type": "revenue",
            "description": stripe_payment.description or "Paiement Stripe",
            "category": "online_payment",
            "source": "stripe",
            "gst_amount": self._calculate_tax_amount(stripe_payment.amount, "GST"),
            "qst_amount": self._calculate_tax_amount(stripe_payment.amount, "QST"),
            "status": stripe_payment.status,
            "currency": stripe_payment.currency,
            "customer_id": stripe_payment.customer,
            "payment_method": stripe_payment.payment_method_types[0] if stripe_payment.payment_method_types else "unknown"
        }
    
    def _convert_subscription_format(self, stripe_subscription: Any) -> Dict[str, Any]:
        """Convertir un abonnement Stripe au format standard"""
        return {
            "id": stripe_subscription.id,
            "date": datetime.fromtimestamp(stripe_subscription.created).isoformat(),
            "amount": float(stripe_subscription.items.data[0].price.unit_amount) / 100,
            "type": "revenue",
            "description": f"Abonnement {stripe_subscription.items.data[0].price.nickname or 'Stripe'}",
            "category": "subscription",
            "source": "stripe",
            "gst_amount": self._calculate_tax_amount(stripe_subscription.items.data[0].price.unit_amount, "GST"),
            "qst_amount": self._calculate_tax_amount(stripe_subscription.items.data[0].price.unit_amount, "QST"),
            "status": stripe_subscription.status,
            "customer_id": stripe_subscription.customer,
            "interval": stripe_subscription.items.data[0].price.recurring.interval if stripe_subscription.items.data[0].price.recurring else "one_time"
        }
    
    def _convert_customer_format(self, stripe_customer: Any) -> Dict[str, Any]:
        """Convertir un client Stripe au format standard"""
        return {
            "id": stripe_customer.id,
            "name": stripe_customer.name or "",
            "email": stripe_customer.email or "",
            "phone": stripe_customer.phone or "",
            "type": "customer",
            "source": "stripe",
            "created_date": datetime.fromtimestamp(stripe_customer.created).isoformat(),
            "status": "active" if not stripe_customer.deleted else "deleted"
        }
    
    def _convert_fee_format(self, stripe_fee: Any) -> Dict[str, Any]:
        """Convertir un frais Stripe au format standard"""
        return {
            "id": stripe_fee.id,
            "date": datetime.fromtimestamp(stripe_fee.created).isoformat(),
            "amount": float(stripe_fee.amount) / 100,
            "type": "expense",
            "description": "Frais de plateforme Stripe",
            "category": "platform_fees",
            "source": "stripe",
            "gst_amount": self._calculate_tax_amount(stripe_fee.amount, "GST"),
            "qst_amount": self._calculate_tax_amount(stripe_fee.amount, "QST"),
            "status": "succeeded",
            "application_fee_id": stripe_fee.id
        }
    
    def _convert_to_transactions(self, synced_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Convertir les données synchronisées en transactions standard"""
        transactions = []
        
        # Ajouter les paiements comme transactions
        for payment in synced_data.get("payments", []):
            transactions.append(payment)
        
        # Ajouter les abonnements comme transactions
        for subscription in synced_data.get("subscriptions", []):
            transactions.append(subscription)
        
        # Ajouter les frais comme transactions
        for fee in synced_data.get("fees", []):
            transactions.append(fee)
        
        return transactions
    
    def _calculate_tax_amount(self, amount_cents: int, tax_type: str) -> float:
        """Calculer le montant de taxe basé sur le type"""
        amount_dollars = amount_cents / 100
        
        if tax_type == "GST":
            return amount_dollars * 0.05  # 5% TPS
        elif tax_type == "QST":
            return amount_dollars * 0.09975  # 9.975% TVQ
        else:
            return 0.0
    
    def get_revenue_breakdown(self) -> Dict[str, Any]:
        """Obtenir la répartition des revenus"""
        if not self.data_cache:
            return {"error": "Aucune donnée disponible"}
        
        payments = self.data_cache.get("payments", [])
        subscriptions = self.data_cache.get("subscriptions", [])
        
        # Calculer les revenus par source
        revenue_sources = {}
        
        for payment in payments:
            source = payment.get("payment_method", "unknown")
            amount = payment.get("amount", 0)
            
            if source not in revenue_sources:
                revenue_sources[source] = 0
            revenue_sources[source] += amount
        
        for subscription in subscriptions:
            source = "subscription"
            amount = subscription.get("amount", 0)
            
            if source not in revenue_sources:
                revenue_sources[source] = 0
            revenue_sources[source] += amount
        
        total_revenue = sum(revenue_sources.values())
        
        return {
            "total_revenue": total_revenue,
            "revenue_sources": revenue_sources,
            "payment_count": len(payments),
            "subscription_count": len(subscriptions),
            "last_sync": self.last_sync.isoformat() if self.last_sync else None
        }
    
    def get_platform_fees_impact(self) -> Dict[str, Any]:
        """Analyser l'impact des frais de plateforme"""
        if not self.data_cache:
            return {"error": "Aucune donnée disponible"}
        
        fees = self.data_cache.get("fees", [])
        
        total_fees = sum(fee.get("amount", 0) for fee in fees)
        total_revenue = sum(fee.get("amount", 0) for fee in fees if fee.get("type") == "revenue")
        
        fee_ratio = (total_fees / total_revenue * 100) if total_revenue > 0 else 0
        
        return {
            "total_fees": total_fees,
            "total_revenue": total_revenue,
            "fee_ratio": fee_ratio,
            "fee_count": len(fees),
            "average_fee": total_fees / len(fees) if fees else 0
        }
    
    def get_sync_status(self) -> Dict[str, Any]:
        """Obtenir le statut de synchronisation"""
        return {
            "configured": self.stripe_client is not None,
            "last_sync": self.last_sync.isoformat() if self.last_sync else None,
            "cache_size": len(self.data_cache) if self.data_cache else 0,
            "data_sources": ["payments", "subscriptions", "customers", "fees"] if self.stripe_client else []
        }
    
    def get_subscription_metrics(self) -> Dict[str, Any]:
        """Obtenir les métriques d'abonnement"""
        if not self.data_cache:
            return {"error": "Aucune donnée disponible"}
        
        subscriptions = self.data_cache.get("subscriptions", [])
        
        active_subscriptions = [s for s in subscriptions if s.get("status") == "active"]
        total_mrr = sum(s.get("amount", 0) for s in active_subscriptions)
        
        return {
            "total_subscriptions": len(subscriptions),
            "active_subscriptions": len(active_subscriptions),
            "total_mrr": total_mrr,
            "average_subscription_value": total_mrr / len(active_subscriptions) if active_subscriptions else 0
        } 
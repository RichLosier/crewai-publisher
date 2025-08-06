"""
Configuration principale du système fiscal AI
"""
import os
from typing import Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
import pytz
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

@dataclass
class CompanyConfig:
    """Configuration de l'entreprise"""
    name: str = "iFiveMe"
    qst_number: Optional[str] = None
    gst_number: Optional[str] = None
    fiscal_year_end: str = "12-31"
    province: str = "QC"
    country: str = "CA"
    timezone: str = "America/Montreal"

@dataclass
class APIConfig:
    """Configuration des APIs"""
    xero_client_id: Optional[str] = None
    xero_client_secret: Optional[str] = None
    stripe_secret_key: Optional[str] = None
    desjardins_api_key: Optional[str] = None
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None

@dataclass
class SecurityConfig:
    """Configuration de sécurité"""
    encryption_key: Optional[str] = None
    database_url: Optional[str] = None
    enable_audit_logging: bool = True
    data_retention_days: int = 730  # 2 ans

@dataclass
class LearningConfig:
    """Configuration d'apprentissage"""
    enable_learning: bool = True
    learning_data_retention: str = "2_years"
    enable_predictive_analytics: bool = True
    enable_real_time_sync: bool = True

@dataclass
class TaxConfig:
    """Configuration fiscale"""
    # Taux de taxes Québec
    qst_rate: float = 0.09975  # 9.975%
    gst_rate: float = 0.05     # 5%
    
    # Seuils et limites
    small_business_threshold: float = 30000.0
    qst_threshold: float = 30000.0
    
    # Échéances importantes
    quarterly_deadlines: list = None
    annual_deadlines: list = None
    
    def __post_init__(self):
        if self.quarterly_deadlines is None:
            self.quarterly_deadlines = [
                "04-30", "07-31", "10-31", "01-31"
            ]
        if self.annual_deadlines is None:
            self.annual_deadlines = [
                "04-30", "06-15"
            ]

class FiscalAIConfig:
    """Configuration principale du système fiscal AI"""
    
    def __init__(self):
        self.company = CompanyConfig(
            name=os.getenv("COMPANY_NAME", "iFiveMe"),
            qst_number=os.getenv("COMPANY_QST_NUMBER"),
            gst_number=os.getenv("COMPANY_GST_NUMBER"),
            fiscal_year_end=os.getenv("FISCAL_YEAR_END", "12-31")
        )
        
        self.api = APIConfig(
            xero_client_id=os.getenv("XERO_CLIENT_ID"),
            xero_client_secret=os.getenv("XERO_CLIENT_SECRET"),
            stripe_secret_key=os.getenv("STRIPE_SECRET_KEY"),
            desjardins_api_key=os.getenv("DESJARDINS_API_KEY"),
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            anthropic_api_key=os.getenv("ANTHROPIC_API_KEY")
        )
        
        self.security = SecurityConfig(
            encryption_key=os.getenv("ENCRYPTION_KEY"),
            database_url=os.getenv("DATABASE_URL"),
            enable_audit_logging=os.getenv("ENABLE_AUDIT_LOGGING", "true").lower() == "true",
            data_retention_days=int(os.getenv("DATA_RETENTION_DAYS", "730"))
        )
        
        self.learning = LearningConfig(
            enable_learning=os.getenv("ENABLE_LEARNING", "true").lower() == "true",
            learning_data_retention=os.getenv("LEARNING_DATA_RETENTION", "2_years"),
            enable_predictive_analytics=os.getenv("ENABLE_PREDICTIVE_ANALYTICS", "true").lower() == "true",
            enable_real_time_sync=os.getenv("ENABLE_REAL_TIME_SYNC", "true").lower() == "true"
        )
        
        self.tax = TaxConfig()
        
        # Configuration des timezones
        self.timezone = pytz.timezone(self.company.timezone)
        
        # Configuration des chemins
        self.base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.data_path = os.path.join(self.base_path, "data")
        self.templates_path = os.path.join(self.data_path, "templates")
        self.knowledge_base_path = os.path.join(self.data_path, "knowledge_base")
        self.learning_data_path = os.path.join(self.data_path, "learning_data")
        
        # Créer les répertoires si ils n'existent pas
        os.makedirs(self.data_path, exist_ok=True)
        os.makedirs(self.templates_path, exist_ok=True)
        os.makedirs(self.knowledge_base_path, exist_ok=True)
        os.makedirs(self.learning_data_path, exist_ok=True)
    
    def validate_config(self) -> Dict[str, Any]:
        """Valider la configuration et retourner les erreurs"""
        errors = []
        warnings = []
        
        # Validation des APIs requises
        if not self.api.xero_client_id:
            errors.append("XERO_CLIENT_ID manquant")
        if not self.api.xero_client_secret:
            errors.append("XERO_CLIENT_SECRET manquant")
        if not self.api.stripe_secret_key:
            warnings.append("STRIPE_SECRET_KEY manquant - certaines fonctionnalités seront limitées")
        if not self.api.openai_api_key:
            errors.append("OPENAI_API_KEY manquant")
        
        # Validation de la configuration entreprise
        if not self.company.qst_number:
            warnings.append("COMPANY_QST_NUMBER manquant - certaines fonctionnalités québécoises seront limitées")
        if not self.company.gst_number:
            warnings.append("COMPANY_GST_NUMBER manquant - certaines fonctionnalités fédérales seront limitées")
        
        # Validation de la sécurité
        if not self.security.encryption_key:
            warnings.append("ENCRYPTION_KEY manquant - les données ne seront pas chiffrées")
        if not self.security.database_url:
            warnings.append("DATABASE_URL manquant - utilisation du stockage local")
        
        return {
            "errors": errors,
            "warnings": warnings,
            "is_valid": len(errors) == 0
        }
    
    def get_current_fiscal_year(self) -> int:
        """Obtenir l'année fiscale actuelle"""
        now = datetime.now(self.timezone)
        fiscal_year_end = datetime.strptime(self.company.fiscal_year_end, "%m-%d")
        fiscal_year_end = fiscal_year_end.replace(year=now.year)
        
        if now.date() < fiscal_year_end.date():
            return now.year - 1
        else:
            return now.year
    
    def get_fiscal_period(self) -> Dict[str, datetime]:
        """Obtenir la période fiscale actuelle"""
        current_year = self.get_current_fiscal_year()
        fiscal_end = datetime.strptime(f"{current_year}-{self.company.fiscal_year_end}", "%Y-%m-%d")
        fiscal_start = fiscal_end.replace(year=fiscal_end.year - 1) + timedelta(days=1)
        
        return {
            "start": fiscal_start,
            "end": fiscal_end,
            "year": current_year
        }
    
    def is_quarterly_deadline_approaching(self, days_ahead: int = 30) -> bool:
        """Vérifier si une échéance trimestrielle approche"""
        now = datetime.now(self.timezone)
        current_month = now.month
        
        # Déterminer la prochaine échéance trimestrielle
        if current_month <= 3:
            next_deadline = datetime(now.year, 4, 30)
        elif current_month <= 6:
            next_deadline = datetime(now.year, 7, 31)
        elif current_month <= 9:
            next_deadline = datetime(now.year, 10, 31)
        else:
            next_deadline = datetime(now.year + 1, 1, 31)
        
        days_until_deadline = (next_deadline - now).days
        return days_until_deadline <= days_ahead

# Instance globale de configuration
config = FiscalAIConfig() 
"""
Calendrier fiscal pour le Québec et le Canada
"""
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass
import pytz
from config.settings import config

@dataclass
class FiscalDeadline:
    """Représente une échéance fiscale"""
    name: str
    date: datetime
    description: str
    type: str  # 'quarterly', 'annual', 'monthly', 'special'
    jurisdiction: str  # 'QC', 'CA', 'both'
    priority: str = 'normal'  # 'high', 'normal', 'low'
    is_automatic: bool = False  # Si la soumission est automatique

class FiscalCalendar:
    """Calendrier fiscal complet pour iFiveMe"""
    
    def __init__(self):
        self.timezone = pytz.timezone(config.company.timezone)
        self.current_year = datetime.now(self.timezone).year
        
    def get_quarterly_deadlines(self, year: Optional[int] = None) -> List[FiscalDeadline]:
        """Obtenir toutes les échéances trimestrielles pour une année"""
        if year is None:
            year = self.current_year
            
        deadlines = [
            FiscalDeadline(
                name="Déclaration TPS/TVH Q1",
                date=datetime(year, 4, 30, tzinfo=self.timezone),
                description="Déclaration trimestrielle TPS/TVH pour Q1 (janvier-mars)",
                type="quarterly",
                jurisdiction="both",
                priority="high",
                is_automatic=True
            ),
            FiscalDeadline(
                name="Déclaration TPS/TVH Q2",
                date=datetime(year, 7, 31, tzinfo=self.timezone),
                description="Déclaration trimestrielle TPS/TVH pour Q2 (avril-juin)",
                type="quarterly",
                jurisdiction="both",
                priority="high",
                is_automatic=True
            ),
            FiscalDeadline(
                name="Déclaration TPS/TVH Q3",
                date=datetime(year, 10, 31, tzinfo=self.timezone),
                description="Déclaration trimestrielle TPS/TVH pour Q3 (juillet-septembre)",
                type="quarterly",
                jurisdiction="both",
                priority="high",
                is_automatic=True
            ),
            FiscalDeadline(
                name="Déclaration TPS/TVH Q4",
                date=datetime(year + 1, 1, 31, tzinfo=self.timezone),
                description="Déclaration trimestrielle TPS/TVH pour Q4 (octobre-décembre)",
                type="quarterly",
                jurisdiction="both",
                priority="high",
                is_automatic=True
            )
        ]
        
        return deadlines
    
    def get_annual_deadlines(self, year: Optional[int] = None) -> List[FiscalDeadline]:
        """Obtenir toutes les échéances annuelles pour une année"""
        if year is None:
            year = self.current_year
            
        deadlines = [
            FiscalDeadline(
                name="Déclaration de revenus T1",
                date=datetime(year + 1, 4, 30, tzinfo=self.timezone),
                description="Déclaration de revenus fédérale pour l'année civile",
                type="annual",
                jurisdiction="CA",
                priority="high",
                is_automatic=False
            ),
            FiscalDeadline(
                name="Déclaration de revenus TP-1",
                date=datetime(year + 1, 4, 30, tzinfo=self.timezone),
                description="Déclaration de revenus québécoise pour l'année civile",
                type="annual",
                jurisdiction="QC",
                priority="high",
                is_automatic=False
            ),
            FiscalDeadline(
                name="Déclaration TPS/TVH annuelle",
                date=datetime(year + 1, 6, 15, tzinfo=self.timezone),
                description="Déclaration annuelle TPS/TVH (si applicable)",
                type="annual",
                jurisdiction="both",
                priority="normal",
                is_automatic=True
            ),
            FiscalDeadline(
                name="Déclaration T2 (si applicable)",
                date=datetime(year + 1, 6, 15, tzinfo=self.timezone),
                description="Déclaration de revenus corporative T2",
                type="annual",
                jurisdiction="CA",
                priority="normal",
                is_automatic=False
            )
        ]
        
        return deadlines
    
    def get_monthly_deadlines(self, year: Optional[int] = None, month: Optional[int] = None) -> List[FiscalDeadline]:
        """Obtenir les échéances mensuelles"""
        if year is None:
            year = self.current_year
        if month is None:
            month = datetime.now(self.timezone).month
            
        # Vérifier que le mois est valide
        if month < 1 or month > 12:
            return []
            
        # Déterminer le dernier jour du mois
        if month == 12:
            next_month = datetime(year + 1, 1, 1)
        else:
            next_month = datetime(year, month + 1, 1)
        last_day = (next_month - timedelta(days=1)).day
            
        deadlines = [
            FiscalDeadline(
                name="Retenues à la source",
                date=datetime(year, month, 15, tzinfo=self.timezone),
                description="Paiement des retenues à la source (si applicable)",
                type="monthly",
                jurisdiction="both",
                priority="normal",
                is_automatic=True
            ),
            FiscalDeadline(
                name="Déclaration TPS/TVH mensuelle",
                date=datetime(year, month, last_day, tzinfo=self.timezone),
                description="Déclaration mensuelle TPS/TVH (si applicable)",
                type="monthly",
                jurisdiction="both",
                priority="normal",
                is_automatic=True
            )
        ]
        
        return deadlines
    
    def get_special_deadlines(self, year: Optional[int] = None) -> List[FiscalDeadline]:
        """Obtenir les échéances spéciales"""
        if year is None:
            year = self.current_year
            
        deadlines = [
            FiscalDeadline(
                name="Installations TPS/TVH",
                date=datetime(year, 3, 31, tzinfo=self.timezone),
                description="Paiement des installations TPS/TVH",
                type="special",
                jurisdiction="both",
                priority="high",
                is_automatic=True
            ),
            FiscalDeadline(
                name="Installations impôt sur le revenu",
                date=datetime(year, 3, 31, tzinfo=self.timezone),
                description="Paiement des installations d'impôt sur le revenu",
                type="special",
                jurisdiction="both",
                priority="high",
                is_automatic=True
            )
        ]
        
        return deadlines
    
    def get_all_deadlines(self, year: Optional[int] = None) -> List[FiscalDeadline]:
        """Obtenir toutes les échéances pour une année"""
        if year is None:
            year = self.current_year
            
        all_deadlines = []
        all_deadlines.extend(self.get_quarterly_deadlines(year))
        all_deadlines.extend(self.get_annual_deadlines(year))
        all_deadlines.extend(self.get_special_deadlines(year))
        
        # Ajouter les échéances mensuelles pour chaque mois
        for month in range(1, 13):
            all_deadlines.extend(self.get_monthly_deadlines(year, month))
        
        # Trier par date
        all_deadlines.sort(key=lambda x: x.date)
        
        return all_deadlines
    
    def get_upcoming_deadlines(self, days_ahead: int = 30) -> List[FiscalDeadline]:
        """Obtenir les échéances à venir dans les X prochains jours"""
        now = datetime.now(self.timezone)
        all_deadlines = self.get_all_deadlines()
        
        upcoming = []
        for deadline in all_deadlines:
            days_until = (deadline.date - now).days
            if 0 <= days_until <= days_ahead:
                upcoming.append(deadline)
        
        return upcoming
    
    def get_overdue_deadlines(self) -> List[FiscalDeadline]:
        """Obtenir les échéances en retard"""
        now = datetime.now(self.timezone)
        all_deadlines = self.get_all_deadlines()
        
        overdue = []
        for deadline in all_deadlines:
            if deadline.date < now:
                overdue.append(deadline)
        
        return overdue
    
    def get_deadline_by_name(self, name: str, year: Optional[int] = None) -> Optional[FiscalDeadline]:
        """Obtenir une échéance spécifique par nom"""
        all_deadlines = self.get_all_deadlines(year)
        
        for deadline in all_deadlines:
            if deadline.name.lower() == name.lower():
                return deadline
        
        return None
    
    def is_deadline_approaching(self, deadline_name: str, days_ahead: int = 30) -> bool:
        """Vérifier si une échéance spécifique approche"""
        deadline = self.get_deadline_by_name(deadline_name)
        if not deadline:
            return False
        
        now = datetime.now(self.timezone)
        days_until = (deadline.date - now).days
        
        return 0 <= days_until <= days_ahead
    
    def get_next_deadline(self) -> Optional[FiscalDeadline]:
        """Obtenir la prochaine échéance"""
        now = datetime.now(self.timezone)
        all_deadlines = self.get_all_deadlines()
        
        future_deadlines = [d for d in all_deadlines if d.date > now]
        if future_deadlines:
            return min(future_deadlines, key=lambda x: x.date)
        
        return None
    
    def get_deadlines_by_type(self, deadline_type: str, year: Optional[int] = None) -> List[FiscalDeadline]:
        """Obtenir les échéances par type"""
        all_deadlines = self.get_all_deadlines(year)
        
        return [d for d in all_deadlines if d.type == deadline_type]
    
    def get_deadlines_by_jurisdiction(self, jurisdiction: str, year: Optional[int] = None) -> List[FiscalDeadline]:
        """Obtenir les échéances par juridiction"""
        all_deadlines = self.get_all_deadlines(year)
        
        return [d for d in all_deadlines if d.jurisdiction in [jurisdiction, 'both']]

# Instance globale du calendrier fiscal
fiscal_calendar = FiscalCalendar() 
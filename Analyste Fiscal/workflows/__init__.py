"""
Module des workflows automatisés pour le système fiscal AI
"""

from .quarterly_workflow import QuarterlyWorkflow
from .annual_workflow import AnnualWorkflow
from .monthly_workflow import MonthlyWorkflow
from .strategic_workflow import StrategicWorkflow

__all__ = [
    'QuarterlyWorkflow',
    'AnnualWorkflow', 
    'MonthlyWorkflow',
    'StrategicWorkflow'
] 
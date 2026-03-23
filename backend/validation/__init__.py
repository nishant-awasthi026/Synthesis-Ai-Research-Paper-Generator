"""Validation package initialization"""

from backend.validation.results_validator import ResultsValidator, validate_notebook_results, validate_csv_results
from backend.validation.ethics_checker import PlagiarismChecker, AIContentDetector, EthicsChecker

__all__ = [
    'ResultsValidator',
    'validate_notebook_results',
    'validate_csv_results',
    'PlagiarismChecker',
    'AIContentDetector',
    'EthicsChecker'
]

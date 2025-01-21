"""
Core shared ledger functionality for credit management.

This package provides the base implementation for a shared ledger system
that can be used across multiple applications.
"""

__version__ = "0.1.0"

from .models.base import Base
from .models.ledger import LedgerEntry
from .operations.base import BaseLedgerOperations, LedgerOperationType
from .schemas.ledger import LedgerEntryCreate, LedgerBalance
from .utils.ledger import get_balance, process_ledger_operation

__all__ = [
    "Base",
    "LedgerEntry",
    "BaseLedgerOperations",
    "LedgerOperationType",
    "LedgerEntryCreate",
    "LedgerBalance",
    "get_balance",
    "process_ledger_operation",
]

"""
Base ledger operations and configuration.
"""

from enum import Enum
from typing import Dict, Set, Literal

# Core operation literals - shared operations that all apps can use
BaseLedgerOperationLiteral = Literal[
    "DAILY_REWARD",
    "SIGNUP_CREDIT",
    "CREDIT_SPEND",
    "CREDIT_ADD"
]

class LedgerOperationType(str, Enum):
    """
    Core ledger operation types.
    These are the shared operations that any credit system can use.
    Applications can extend these with their own specific operations.
    """
    DAILY_REWARD = "DAILY_REWARD"   # Daily reward credit
    SIGNUP_CREDIT = "SIGNUP_CREDIT" # Initial signup bonus
    CREDIT_SPEND = "CREDIT_SPEND"   # Generic credit deduction
    CREDIT_ADD = "CREDIT_ADD"       # Generic credit addition

    @classmethod
    def required_operations(cls) -> Set[str]:
        """Get the set of required core operations."""
        return {
            LedgerOperationType.DAILY_REWARD.value,
            LedgerOperationType.SIGNUP_CREDIT.value,
            LedgerOperationType.CREDIT_SPEND.value,
            LedgerOperationType.CREDIT_ADD.value,
        }


class BaseLedgerOperations:
    """
    Base class for ledger operations configuration.
    Applications should extend this class and add their specific operations.
    """
    
    # Core operation configuration with default values
    BASE_CONFIG: Dict[BaseLedgerOperationLiteral, int] = {
        LedgerOperationType.DAILY_REWARD.value: 1,    # Daily reward amount
        LedgerOperationType.SIGNUP_CREDIT.value: 3,   # Initial signup bonus
        LedgerOperationType.CREDIT_SPEND.value: -1,   # Default spend amount
        LedgerOperationType.CREDIT_ADD.value: 10,     # Default add amount
    }
    
    @classmethod
    def get_operation_config(cls) -> Dict[str, int]:
        """
        Get the complete operation configuration.
        Override this in application-specific classes to add custom operations.
        
        Returns:
            Dict mapping operation names to their credit values
        """
        return cls.BASE_CONFIG.copy()

    @classmethod
    def validate_operations(cls, operations: Set[str]) -> None:
        """
        Validate that all required operations are present.
        Applications can override this to add their own validation.
        
        Args:
            operations: Set of operation names to validate
            
        Raises:
            ValueError: If any required operations are missing
        """
        missing_operations = cls.required_operations() - operations
        if missing_operations:
            raise ValueError(f"Missing required operations: {missing_operations}") 
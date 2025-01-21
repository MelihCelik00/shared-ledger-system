"""
Example app-specific ledger operations.
"""

from enum import Enum
from typing import Dict, Literal

from core.shared_ledger.operations.base import (
    BaseLedgerOperations,
    BaseLedgerOperationLiteral,
    LedgerOperationType
)

# Combine base and app-specific operations
ExampleAppOperationLiteral = Literal[
    BaseLedgerOperationLiteral,
    "CONTENT_CREATION",
    "CONTENT_ACCESS"
]

class ExampleAppOperationType(str, Enum):
    """
    Example app-specific operation types.
    Extends core operations with content-related operations.
    """
    # Include base operations
    DAILY_REWARD = LedgerOperationType.DAILY_REWARD.value
    SIGNUP_CREDIT = LedgerOperationType.SIGNUP_CREDIT.value
    CREDIT_SPEND = LedgerOperationType.CREDIT_SPEND.value
    CREDIT_ADD = LedgerOperationType.CREDIT_ADD.value
    
    # App-specific operations
    CONTENT_CREATION = "CONTENT_CREATION"
    CONTENT_ACCESS = "CONTENT_ACCESS"


class ExampleAppOperations(BaseLedgerOperations):
    """
    Example app operation configuration.
    Extends base operations with content-specific operations and their credit values.
    """
    
    # App-specific operation configuration
    APP_CONFIG: Dict[ExampleAppOperationLiteral, int] = {
        # Content operations with their credit costs
        ExampleAppOperationType.CONTENT_CREATION.value: -5,
        ExampleAppOperationType.CONTENT_ACCESS.value: 0,
    }
    
    @classmethod
    def get_operation_config(cls) -> Dict[str, int]:
        """
        Get the complete operation configuration including base and app-specific operations.
        
        Returns:
            Dict mapping operation names to their credit values
        """
        config = super().get_operation_config()
        config.update(cls.APP_CONFIG)
        return config 
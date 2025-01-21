from enum import Enum
from typing import Dict, Literal, Union

from core.shared_ledger.operations.base import (
    BaseLedgerOperations,
    LedgerOperationType,
    BaseLedgerOperationLiteral
)

# Define literal types for app-specific operations
AppSpecificOperationLiteral = Literal[
    "CONTENT_CREATION",
    "CONTENT_ACCESS",
    "PREMIUM_CONTENT_CREATION"
]

# Combined type for all operations
ExampleAppOperationLiteral = Union[BaseLedgerOperationLiteral, AppSpecificOperationLiteral]

class ExampleAppOperationType(str, Enum):
    """Example application-specific operation types."""
    # Required base operations
    DAILY_REWARD = LedgerOperationType.DAILY_REWARD.value
    SIGNUP_CREDIT = LedgerOperationType.SIGNUP_CREDIT.value
    CREDIT_SPEND = LedgerOperationType.CREDIT_SPEND.value
    CREDIT_ADD = LedgerOperationType.CREDIT_ADD.value
    
    # App-specific operations
    CONTENT_CREATION = "CONTENT_CREATION"
    CONTENT_ACCESS = "CONTENT_ACCESS"
    PREMIUM_CONTENT_CREATION = "PREMIUM_CONTENT_CREATION"

class ExampleAppOperations(BaseLedgerOperations):
    """Example application operations configuration."""
    
    # App-specific operation configuration with specific values
    APP_CONFIG: Dict[AppSpecificOperationLiteral, int] = {
        ExampleAppOperationType.CONTENT_CREATION.value: -5,
        ExampleAppOperationType.CONTENT_ACCESS.value: 0,
        ExampleAppOperationType.PREMIUM_CONTENT_CREATION.value: -10,
    }
    
    @classmethod
    def get_operation_config(cls) -> Dict[str, int]:
        """Get the complete operation configuration including app-specific operations."""
        config = super().get_operation_config()
        return {**config, **cls.APP_CONFIG} 
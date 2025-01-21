"""
Pydantic models for ledger operations.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

class LedgerEntryBase(BaseModel):
    """
    Base Pydantic model for ledger entries.
    
    Attributes:
        operation: Type of ledger operation (e.g., SIGNUP_CREDIT, CONTENT_CREATION)
        owner_id: ID of the entry owner
        amount: Credit amount for the operation. Required in database but optional in POST requests
                as it will be automatically set from the operation configuration.
    """
    operation: str = Field(..., description="Type of ledger operation")
    owner_id: str = Field(..., description="ID of the entry owner")
    amount: Optional[int] = Field(None, description="Credit amount (optional in POST requests, will be taken from operation config)")

class LedgerEntryCreate(LedgerEntryBase):
    """
    Schema for creating a new ledger entry.
    The amount will be determined by the operation type.
    """
    nonce: str = Field(..., description="Unique identifier to prevent duplicate transactions")

class LedgerEntryResponse(BaseModel):
    """
    Schema for ledger entry response.
    """
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    operation: str
    owner_id: str
    amount: int
    nonce: str
    created_at: datetime
    updated_at: datetime

class LedgerBalance(BaseModel):
    """
    Schema for ledger balance response.
    """
    balance: int
    last_updated: Optional[datetime] = None

class LedgerOperationResponse(BaseModel):
    """
    Schema for ledger operation response.
    """
    entry: LedgerEntryResponse
    balance: int 
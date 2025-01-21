"""
Core ledger API router providing basic ledger functionality.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from ..schemas.ledger import (
    LedgerEntryCreate,
    LedgerEntryResponse,
    LedgerBalance,
    LedgerOperationResponse
)
from ..utils.ledger import (
    get_balance,
    process_ledger_operation,
    InsufficientCreditsError,
    DuplicateTransactionError
)
from ..operations.base import BaseLedgerOperations

router = APIRouter(prefix="/ledger", tags=["ledger"])

# Define a placeholder dependency that will be overridden by the app
async def get_db() -> AsyncSession:
    raise NotImplementedError("Database dependency must be overridden by the app")

@router.get(
    "/{owner_id}/balance",
    response_model=LedgerBalance,
    summary="Get owner balance",
    description="Get the current balance for an owner."
)
async def get_owner_balance_handler(
    owner_id: str,
    db: Annotated[AsyncSession, Depends(get_db)]
) -> LedgerBalance:
    """
    Get the current balance for an owner.
    
    Args:
        owner_id: The unique identifier of the owner
        db: The database session
        
    Returns:
        LedgerBalance: The current balance and last update time
    """
    return await get_balance(db, owner_id)

@router.post(
    "/entry",
    response_model=LedgerOperationResponse,
    summary="Create ledger entry",
    description="Create a new ledger entry with the specified operation."
)
async def create_ledger_entry_handler(
    entry: LedgerEntryCreate,
    db: Annotated[AsyncSession, Depends(get_db)]
) -> LedgerOperationResponse:
    """
    Create a new ledger entry.
    
    This endpoint processes ledger operations and updates balances.
    The amount will be taken from the operation configuration.
    
    Args:
        entry: The ledger entry to create
        db: The database session
        
    Returns:
        LedgerOperationResponse: The created ledger entry
        
    Raises:
        HTTPException: If the operation is invalid, insufficient credits, or duplicate transaction
    """
    try:
        return await process_ledger_operation(
            db,
            BaseLedgerOperations,
            entry
        )
    except (ValueError, InsufficientCreditsError, DuplicateTransactionError) as e:
        raise HTTPException(status_code=400, detail=str(e)) 
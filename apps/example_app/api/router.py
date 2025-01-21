from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import uuid

from core.shared_ledger.schemas.ledger import (
    LedgerEntryCreate,
    LedgerEntryResponse,
    LedgerBalance,
    LedgerOperationResponse
)
from core.shared_ledger.utils.ledger import (
    get_balance,
    process_ledger_operation,
    InsufficientCreditsError,
    DuplicateTransactionError
)
from ..operations import ExampleAppOperations, ExampleAppOperationType
from .dependencies import get_db

router = APIRouter(prefix="/ledger", tags=["ledger"])

@router.get("/{owner_id}/balance", response_model=LedgerBalance)
async def get_owner_balance(
    owner_id: str,
    db: AsyncSession = Depends(get_db)
) -> LedgerBalance:
    """Get the current balance for an owner."""
    return await get_balance(db, owner_id)

@router.post("", response_model=LedgerOperationResponse)
async def create_ledger_entry(
    entry: LedgerEntryCreate,
    db: AsyncSession = Depends(get_db)
) -> LedgerOperationResponse:
    """
    Create a new ledger entry.
    
    This endpoint processes ledger operations and updates balances.
    It handles both core operations and app-specific operations.
    The amount will be taken from the operation configuration.
    """
    try:
        return await process_ledger_operation(
            db,
            ExampleAppOperations,
            entry
        )
    except (ValueError, InsufficientCreditsError, DuplicateTransactionError) as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/content/create", response_model=LedgerOperationResponse)
async def create_content(
    owner_id: str,
    is_premium: bool = False,
    db: AsyncSession = Depends(get_db)
) -> LedgerOperationResponse:
    """
    Convenience endpoint for content creation operation.
    Automatically determines the operation type and uses configured credit cost.
    """
    operation = (
        ExampleAppOperationType.PREMIUM_CONTENT_CREATION
        if is_premium
        else ExampleAppOperationType.CONTENT_CREATION
    )
    
    entry = LedgerEntryCreate(
        operation=operation.value,
        owner_id=owner_id,
        nonce=str(uuid.uuid4())
    )
    
    return await create_ledger_entry(entry, db)

@router.post("/content/access/{content_id}", response_model=LedgerOperationResponse)
async def access_content(
    content_id: str,
    owner_id: str,
    db: AsyncSession = Depends(get_db)
) -> LedgerOperationResponse:
    """
    Convenience endpoint for content access operation.
    Records content access in the ledger with configured credit cost.
    """
    entry = LedgerEntryCreate(
        operation=ExampleAppOperationType.CONTENT_ACCESS.value,
        owner_id=owner_id,
        nonce=f"access_{content_id}_{owner_id}_{uuid.uuid4()}"
    )
    
    return await create_ledger_entry(entry, db)

@router.post("/signup/{owner_id}", response_model=LedgerOperationResponse)
async def signup_credit(
    owner_id: str,
    db: AsyncSession = Depends(get_db)
) -> LedgerOperationResponse:
    """
    Create initial signup credit for a new user.
    Uses the SIGNUP_CREDIT operation with its configured value.
    """
    entry = LedgerEntryCreate(
        operation=ExampleAppOperationType.SIGNUP_CREDIT.value,
        owner_id=owner_id,
        nonce=f"signup_{owner_id}_{uuid.uuid4()}"
    )
    
    return await create_ledger_entry(entry, db) 
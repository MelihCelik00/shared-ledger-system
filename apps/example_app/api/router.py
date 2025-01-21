"""
Example app API router providing content-specific ledger operations.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
import uuid

from core.shared_ledger.schemas.ledger import (
    LedgerEntryCreate,
    LedgerOperationResponse
)
from core.shared_ledger.api.router import router as core_ledger_router
from core.shared_ledger.utils.ledger import process_ledger_operation, InsufficientCreditsError, DuplicateTransactionError
from ..operations import ExampleAppOperations, ExampleAppOperationType
from .dependencies import get_db

# Create app-specific router
router = APIRouter(tags=["example_app"])

# Include core ledger router without prefix since it already has one
router.include_router(core_ledger_router, prefix="")

async def create_entry(
    entry: LedgerEntryCreate,
    db: AsyncSession
) -> LedgerOperationResponse:
    """
    Create a ledger entry using example app operations.
    """
    try:
        return await process_ledger_operation(
            db,
            ExampleAppOperations,
            entry
        )
    except (ValueError, InsufficientCreditsError, DuplicateTransactionError) as e:
        raise HTTPException(status_code=400, detail=str(e))

# App-specific endpoints
@router.post(
    "/daily-reward",
    response_model=LedgerOperationResponse,
    summary="Claim daily reward",
    description="Claim the daily reward credits for an owner."
)
async def daily_reward(
    owner_id: str,
    db: Annotated[AsyncSession, Depends(get_db)]
) -> LedgerOperationResponse:
    """
    Convenience endpoint for claiming daily reward.
    Uses the configured daily reward amount.
    """
    entry = LedgerEntryCreate(
        operation=ExampleAppOperationType.DAILY_REWARD.value,
        owner_id=owner_id,
        nonce=f"daily_reward_{owner_id}_{uuid.uuid4()}"
    )
    
    return await create_entry(entry, db)

@router.post(
    "/signup",
    response_model=LedgerOperationResponse,
    summary="Get signup credit",
    description="Get the initial signup bonus credits for an owner."
)
async def signup_credit(
    owner_id: str,
    db: Annotated[AsyncSession, Depends(get_db)]
) -> LedgerOperationResponse:
    """
    Convenience endpoint for signup credit.
    Uses the configured signup bonus amount.
    """
    entry = LedgerEntryCreate(
        operation=ExampleAppOperationType.SIGNUP_CREDIT.value,
        owner_id=owner_id,
        nonce=f"signup_{owner_id}"
    )
    
    return await create_entry(entry, db)

@router.post(
    "/content",
    response_model=LedgerOperationResponse,
    summary="Create content",
    description="Create new content and deduct the required credits."
)
async def create_content(
    owner_id: str,
    db: Annotated[AsyncSession, Depends(get_db)]
) -> LedgerOperationResponse:
    """
    Convenience endpoint for content creation operation.
    Uses configured credit cost.
    """
    entry = LedgerEntryCreate(
        operation=ExampleAppOperationType.CONTENT_CREATION.value,
        owner_id=owner_id,
        nonce=str(uuid.uuid4())
    )
    
    return await create_entry(entry, db)

@router.post(
    "/content/{content_id}/access",
    response_model=LedgerOperationResponse,
    summary="Access content",
    description="Access existing content and deduct the required credits."
)
async def access_content(
    content_id: str,
    owner_id: str,
    db: Annotated[AsyncSession, Depends(get_db)]
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
    
    return await create_entry(entry, db)
"""
Example app using the shared ledger system.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.router import router
from .api.dependencies import get_db
from core.shared_ledger.api.router import router as ledger_router
from core.shared_ledger.api.router import get_db as core_get_db

app = FastAPI(
    title="Example Ledger App",
    description="Example application using the shared ledger system",
    version="0.1.0"
)

# Override core dependencies
app.dependency_overrides[core_get_db] = get_db

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(router)
app.include_router(ledger_router)

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"} 
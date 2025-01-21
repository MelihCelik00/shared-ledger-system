"""
Example application demonstrating the usage of shared ledger system.

This app showcases how to:
1. Define custom ledger operations
2. Implement content-based credit system
3. Handle API endpoints with FastAPI
"""

__version__ = "0.1.0"

from .operations import ExampleAppOperations, ExampleAppOperationType
from .api.router import router as example_app_router

__all__ = [
    "ExampleAppOperations",
    "ExampleAppOperationType",
    "example_app_router",
] 
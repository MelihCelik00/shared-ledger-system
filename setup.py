from setuptools import setup, find_namespace_packages

setup(
    name="shared-ledger-system",
    version="0.1.0",
    packages=find_namespace_packages(include=["core.*", "apps.*"]),
    install_requires=[
        "fastapi>=0.104.0",
        "uvicorn>=0.24.0",
        "sqlalchemy>=2.0.0",
        "pydantic>=2.0.0",
        "alembic>=1.12.0",
        "asyncpg>=0.29.0",
    ],
    extras_require={
        "test": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "httpx>=0.24.0",
        ],
    },
) 
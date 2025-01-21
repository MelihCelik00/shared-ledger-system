# System Architecture

This document provides a detailed view of the Shared Ledger System's architecture using various diagrams.

## Core Models

The following class diagram shows the main components of the ledger system and their relationships:

```mermaid
classDiagram
    class LedgerEntry {
        +int id
        +str operation
        +str owner_id
        +int amount
        +str nonce
        +datetime created_at
        +datetime updated_at
    }
    
    class LedgerOperationType {
        +DAILY_REWARD
        +SIGNUP_CREDIT
        +CREDIT_SPEND
        +CREDIT_ADD
    }
    
    class BaseLedgerOperations {
        +Dict BASE_CONFIG
        +get_operation_config()
        +validate_operations()
    }
    
    class ExampleAppOperations {
        +Dict APP_CONFIG
        +get_operation_config()
    }
    
    BaseLedgerOperations <|-- ExampleAppOperations
    LedgerEntry --> LedgerOperationType : uses
```

## Operation Flow

This sequence diagram illustrates the flow of a ledger operation from request to response:

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {
      'primaryColor': '#BB2528',
      'primaryTextColor': '#fff',
      'primaryBorderColor': '#7C0000',
      'lineColor': '#F8B229',
      'secondaryColor': '#006100',
      'tertiaryColor': '#fff'
    }}}%%
sequenceDiagram
    participant Client
    participant FastAPI
    participant LedgerRouter
    participant OperationProcessor
    participant Database

    Client->>FastAPI: POST /ledger/entry
    FastAPI->>LedgerRouter: process_request()
    LedgerRouter->>OperationProcessor: validate_operation()
    OperationProcessor->>Database: check_duplicate_nonce()
    Database-->>OperationProcessor: result
    OperationProcessor->>Database: get_current_balance()
    Database-->>OperationProcessor: balance
    OperationProcessor->>Database: save_entry()
    Database-->>OperationProcessor: success
    OperationProcessor-->>LedgerRouter: operation_result
    LedgerRouter-->>FastAPI: response
    FastAPI-->>Client: 200 OK
```

## System Components

The component diagram below shows how different parts of the system interact:

```mermaid
graph TB
    subgraph "Example App"
        A[FastAPI App]
        B[App Router]
        C[App Operations]
    end
    
    subgraph "Core Ledger System"
        D[Ledger Router]
        E[Operation Processor]
        F[Models & Schemas]
    end
    
    subgraph "Database"
        G[PostgreSQL]
        H[Alembic Migrations]
    end
    
    A --> B
    B --> C
    B --> D
    D --> E
    E --> F
    F --> G
    H --> G
```

## Transaction States

The state diagram shows the lifecycle of a ledger transaction:

```mermaid
stateDiagram-v2
    [*] --> Received
    Received --> Validating: Check Operation
    Validating --> CheckingNonce: Valid Operation
    Validating --> Failed: Invalid Operation
    CheckingNonce --> CheckingBalance: Unique Nonce
    CheckingNonce --> Failed: Duplicate Nonce
    CheckingBalance --> Processing: Sufficient Balance
    CheckingBalance --> Failed: Insufficient Balance
    Processing --> Completed: Save Entry
    Processing --> Failed: Database Error
    Completed --> [*]
    Failed --> [*]
```

## Key Design Decisions

1. **Modular Architecture**
   - Core ledger functionality is separated from application-specific code
   - Applications can extend base operations while maintaining type safety
   - Shared database models and schemas ensure consistency

2. **Transaction Safety**
   - Nonce-based duplicate prevention
   - Balance checks before processing
   - Atomic database operations
   - Comprehensive error handling

3. **Scalability**
   - Asynchronous operations throughout
   - Efficient database queries
   - Connection pooling
   - Modular design for easy extension

4. **Developer Experience**
   - Clear separation of concerns
   - Type-safe operations
   - Comprehensive testing
   - Detailed documentation
   - Docker-based development environment 
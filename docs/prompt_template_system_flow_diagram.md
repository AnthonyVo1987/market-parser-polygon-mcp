# Prompt Template System Flow Diagram

## Complete System Architecture

```mermaid
graph TB
    subgraph "Frontend Layer"
        A[User Input] --> B{Input Type}
        B -->|Direct Chat| C[ChatInput Component]
        B -->|Button Click| D[AnalysisButton Component]
        
        C --> E[Message Validation]
        D --> F[Template Substitution]
        F --> G[Prompt Generation]
        G --> H[Input Population]
        H --> E
        
        E --> I[API Request to /chat]
        
        subgraph "State Management"
            J[useReducer State]
            K[Message Array]
            L[Loading State]
            M[Error State]
        end
        
        I --> J
        J --> K
        J --> L
        J --> M
    end
    
    subgraph "API Layer"
        I --> N[FastAPI Backend]
        N --> O[Chat Endpoint]
        O --> P[Input Validation]
        P --> Q[process_financial_query]
    end
    
    subgraph "Core Processing Layer"
        Q --> R{Cache Check}
        R -->|Hit| S[Return Cached Response]
        R -->|Miss| T[Guardrail Check]
        
        T --> U{Finance Related?}
        U -->|No| V[Guardrail Error Response]
        U -->|Yes| W[Create Analysis Agent]
        
        W --> X[Run Agent with MCP Server]
        X --> Y[Generate Response]
        Y --> Z[Cache Response]
        Z --> AA[Return to Frontend]
        
        S --> AA
        V --> AA
    end
    
    subgraph "External Services"
        X --> BB[Polygon.io MCP Server]
        BB --> CC[Financial Data API]
        X --> DD[OpenAI GPT Model]
        DD --> EE[AI Response Generation]
    end
    
    subgraph "Data Layer"
        FF[SQLite Session]
        GG[Response Cache]
        HH[Configuration]
        
        Q --> FF
        Z --> GG
        W --> HH
    end
    
    AA --> II[Update UI State]
    II --> JJ[Display Response]
    JJ --> KK[User Sees Result]
```

## Detailed Component Interactions

### 1. User Input Flow

```mermaid
sequenceDiagram
    participant U as User
    participant CI as ChatInput
    participant CB as ChatInterface
    participant API as API Service
    participant BE as Backend
    participant AG as Agent
    
    U->>CI: Types message
    CI->>CB: handleSendMessage()
    CB->>API: sendChatMessage()
    API->>BE: POST /chat
    BE->>AG: process_financial_query()
    AG->>AG: Check cache
    AG->>AG: Validate guardrail
    AG->>AG: Run analysis
    AG->>BE: Return response
    BE->>API: ChatResponse
    API->>CB: Update state
    CB->>CI: Display message
    CI->>U: Show response
```

### 2. Button Prompt Flow

```mermaid
sequenceDiagram
    participant U as User
    participant AB as AnalysisButton
    participant CB as ChatInterface
    participant CI as ChatInput
    participant API as API Service
    participant BE as Backend
    participant AG as Agent
    
    U->>AB: Clicks button
    AB->>AB: Template substitution
    AB->>CB: onPromptGenerated()
    CB->>CI: Update input field
    U->>CI: Reviews & sends
    CI->>CB: handleSendMessage()
    CB->>API: sendChatMessage()
    API->>BE: POST /chat
    BE->>AG: process_financial_query()
    AG->>AG: Process query
    AG->>BE: Return response
    BE->>API: ChatResponse
    API->>CB: Update state
    CB->>CI: Display message
    CI->>U: Show response
```

## System Components Detail

### Frontend Components

```mermaid
graph LR
    subgraph "React Components"
        A[ChatInterface_OpenAI]
        B[ChatInput_OpenAI]
        C[AnalysisButton]
        D[SharedTickerInput]
        E[DebugPanel]
    end
    
    subgraph "Hooks & Services"
        F[usePromptAPI]
        G[useInteractionLogger]
        H[usePerformanceLogger]
        I[api_OpenAI]
    end
    
    subgraph "State Management"
        J[useReducer]
        K[Message State]
        L[Loading State]
        M[Error State]
    end
    
    A --> B
    A --> C
    A --> D
    A --> E
    A --> F
    A --> G
    A --> H
    A --> I
    A --> J
    J --> K
    J --> L
    J --> M
```

### Backend Architecture

```mermaid
graph TB
    subgraph "FastAPI Application"
        A[main.py]
        B[API Endpoints]
        C[Middleware]
        D[Lifespan Management]
    end
    
    subgraph "Core Services"
        E[PromptTemplateManager]
        F[TickerExtractor]
        G[process_financial_query]
        H[Guardrail System]
    end
    
    subgraph "External Integrations"
        I[Polygon.io MCP]
        J[OpenAI API]
        K[SQLite Session]
    end
    
    subgraph "Data Layer"
        L[Response Cache]
        M[Configuration]
        N[Logging System]
    end
    
    A --> B
    A --> C
    A --> D
    B --> E
    B --> F
    B --> G
    G --> H
    G --> I
    G --> J
    G --> K
    G --> L
    A --> M
    A --> N
```

## Data Flow Patterns

### 1. Template Processing

```mermaid
flowchart TD
    A[Template Request] --> B[PromptTemplateManager]
    B --> C[Extract Ticker Context]
    C --> D[Select Template Type]
    D --> E[Generate Conversational Prompt]
    E --> F[Add Formatting Instructions]
    F --> G[Add Example Response]
    G --> H[Return Complete Prompt]
```

### 2. Caching Strategy

```mermaid
flowchart TD
    A[Query Request] --> B[Generate Cache Key]
    B --> C{Cache Hit?}
    C -->|Yes| D[Return Cached Response]
    C -->|No| E[Process Query]
    E --> F[Generate Response]
    F --> G[Cache Response]
    G --> H[Return Response]
    D --> I[Update Cache Stats]
    H --> I
```

### 3. Error Handling

```mermaid
flowchart TD
    A[Request] --> B[Input Validation]
    B --> C{Valid Input?}
    C -->|No| D[Validation Error]
    C -->|Yes| E[Guardrail Check]
    E --> F{Finance Related?}
    F -->|No| G[Guardrail Error]
    F -->|Yes| H[Process Query]
    H --> I{Success?}
    I -->|No| J[Processing Error]
    I -->|Yes| K[Success Response]
    
    D --> L[Error Response]
    G --> L
    J --> L
    K --> M[Success Response]
```

## Performance Optimization Points

### 1. Frontend Optimizations

```mermaid
graph LR
    A[Lazy Loading] --> B[Component Splitting]
    B --> C[useReducer State]
    C --> D[useMemo Calculations]
    D --> E[useCallback Handlers]
    E --> F[Performance Monitoring]
```

### 2. Backend Optimizations

```mermaid
graph LR
    A[Response Caching] --> B[Session Management]
    B --> C[Connection Pooling]
    C --> D[Async Processing]
    D --> E[Memory Management]
    E --> F[Logging Optimization]
```

## Security Flow

```mermaid
flowchart TD
    A[User Input] --> B[Input Sanitization]
    B --> C[XSS Prevention]
    C --> D[Length Validation]
    D --> E[Content Filtering]
    E --> F[API Request]
    F --> G[CORS Check]
    G --> H[Rate Limiting]
    H --> I[Authentication]
    I --> J[Authorization]
    J --> K[Process Request]
```

This comprehensive flow diagram shows the complete architecture and data flow of the prompt template system, from user input through all processing layers to the final response display.
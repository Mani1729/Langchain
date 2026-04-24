# LangChain Barber Agent Repository Summary

## Overview
LangChain Barber Agent demonstrates a production-ready AI booking assistant for barbershop services. It showcases middleware patterns, human-in-the-loop workflows, real-world business logic, and complete end-to-end implementation from agent to database.

## Repository Purpose
- Demonstrate production-ready agent system
- Showcase middleware integration patterns
- Illustrate human-in-the-loop oversight
- Implement real-world business logic
- Provide database schema examples
- Show FastAPI + LangGraph integration

## Key Concepts

### Middleware-Integrated Architecture
- Business rules enforcement via middleware
- Conversation summarization for context
- PII masking for privacy
- Usage tracking for monitoring
- Human approval for critical operations

### Human-in-the-Loop Workflow
- Pause execution for critical decisions
- Get human approval before booking
- Validate business policies
- Collect additional information when needed

### Business Rules Engine
- Booking policy enforcement (2-hour notice, 24-hour cancellation)
- Barber availability checking
- Service pricing
- Customer preferences

### Multi-Tool System
- Tool integration for booking operations
- Data consistency checks
- Error handling and recovery
- Transaction-like semantics

## Technology Stack

| Layer | Technology |
|-------|-----------|
| **Agent** | LangChain, LangGraph |
| **LLM** | OpenAI GPT-4-mini |
| **API** | FastAPI, Uvicorn |
| **Database** | SQLAlchemy, SQLite/PostgreSQL |
| **UI** | Chainlit (conversational) |
| **Async** | asyncpg, aiosqlite |
| **Migrations** | Alembic |
| **Testing** | pytest |

## High-Level Architecture

```
┌──────────────────────────────────┐
│      User / Chatlit UI           │
│   (Conversational Interface)     │
└────────────────┬─────────────────┘
                 │
        ┌────────▼──────────────┐
        │  LangGraph Agent      │
        │  ┌──────────────────┐ │
        │  │ Agent Logic      │ │
        │  │ - Understand     │ │
        │  │ - Plan booking   │ │
        │  │ - Execute tools  │ │
        │  └──────────────────┘ │
        └──────────┬────────────┘
                   │
        ┌──────────▼────────────┐
        │  Middleware Stack      │
        ├───────────────────────┤
        │  1. BusinessRules     │
        │  2. ConvSummary       │
        │  3. PII Masking       │
        │  4. UsageTracking     │
        │  5. HumanInTheLoop    │
        └──────────┬────────────┘
                   │
        ┌──────────▼────────────┐
        │  Tool Execution       │
        │  ┌──────────────────┐ │
        │  │ Availability     │ │
        │  │ Booking          │ │
        │  │ Modification     │ │
        │  │ Cancellation     │ │
        │  └──────────────────┘ │
        └──────────┬────────────┘
                   │
        ┌──────────▼────────────┐
        │  FastAPI Backend      │
        │  ┌──────────────────┐ │
        │  │ REST API Routes  │ │
        │  │ Data Validation  │ │
        │  │ Error Handling   │ │
        │  └──────────────────┘ │
        └──────────┬────────────┘
                   │
        ┌──────────▼────────────┐
        │  SQLAlchemy ORM       │
        │  ┌──────────────────┐ │
        │  │ Model Layer      │ │
        │  │ Query Builder    │ │
        │  │ Transactions     │ │
        │  └──────────────────┘ │
        └──────────┬────────────┘
                   │
        ┌──────────▼────────────┐
        │  Database             │
        │  - Customers          │
        │  - Barbers            │
        │  - Services           │
        │  - Bookings           │
        │  - Business Rules     │
        └───────────────────────┘
```

## Design Patterns

### 1. **Middleware-Enhanced Tools**
- Each tool wrapped with business logic
- Middleware composition for concerns
- Clear separation of logic layers
- Reusable middleware across tools

### 2. **Human-in-the-Loop Pattern**
- Pause before critical operations
- Collect human approval
- Validate policies with human oversight
- Prevent unintended bookings

### 3. **Business Rules as Middleware**
- Enforce booking policies
- Check availability constraints
- Validate pricing rules
- Apply discounts programmatically

### 4. **Conversation Management**
- Summarize long conversations
- Manage context window
- Track conversation history
- Extract key booking details

### 5. **PII Protection**
- Mask sensitive data
- Prevent exposure in logs
- Clean user information
- Maintain privacy compliance

## Main Features

1. **Booking Management**: Create, modify, cancel bookings
2. **Availability Checking**: Real-time barber and service availability
3. **Business Rules**: 2-hour notice, 24-hour cancellation policies
4. **Conversational Interface**: Natural language booking via Chainlit
5. **Middleware Stack**: 5-component composition
6. **Human Approval**: HITL for sensitive operations
7. **PII Masking**: Automatic privacy protection
8. **Usage Tracking**: Monitor token consumption
9. **RESTful API**: Full CRUD operations
10. **Type Safety**: SQLAlchemy models with type hints

## Database Schema

```
Tables:
├── customers
│   ├── id (PK)
│   ├── name
│   ├── email
│   ├── phone
│   └── preferences
├── barbers
│   ├── id (PK)
│   ├── name
│   ├── specialties
│   └── availability
├── services
│   ├── id (PK)
│   ├── name
│   ├── duration (minutes)
│   ├── price
│   └── barber_id (FK)
├── bookings
│   ├── id (PK)
│   ├── customer_id (FK)
│   ├── barber_id (FK)
│   ├── service_id (FK)
│   ├── start_time
│   ├── end_time
│   ├── status
│   └── notes
└── business_rules
    ├── id (PK)
    ├── rule_type
    ├── value
    └── description
```

## Middleware Stack Details

| Middleware | Purpose | Responsibility |
|-----------|---------|-----------------|
| **BusinessRules** | Policy enforcement | Check 2-hour notice, 24-hour cancellation |
| **ConvSummary** | Context management | Summarize long conversations |
| **PIIMiddleware** | Email masking | Mask user emails in logs |
| **PIIMiddleware** | Card masking | Mask credit card numbers |
| **UsageTracking** | Monitoring | Count tokens used |
| **HumanInTheLoop** | Approval | Require approval for bookings |

## Tool Definitions (8 Custom Tools)

### 1. check_availability
- Query available time slots
- Parameters: barber_id, service_id, date
- Returns: available slots

### 2. get_barbers
- List all barbers
- Returns: barber list with specialties

### 3. get_services
- List all services
- Parameters: optional barber_id
- Returns: services and pricing

### 4. lookup_customer
- Find customer by email/phone
- Returns: customer details

### 5. create_booking (HITL)
- Create new booking
- Requires human approval
- Checks business rules
- Confirms availability

### 6. modify_booking (HITL)
- Update existing booking
- Requires human approval
- Validates new time slot
- Checks cancellation policy

### 7. cancel_booking (HITL)
- Delete booking
- Requires human approval
- Checks cancellation deadline
- Updates barber availability

### 8. check_policies
- Query business rules
- Returns: applicable policies
- Explains constraints

## File Structure

```
langchain-barber-agent/
├── src/
│   ├── agent/
│   │   ├── agent.py              # Core agent logic
│   │   ├── graph.py              # LangGraph state
│   │   ├── prompt.py             # System prompts
│   │   └── tools.py              # Tool definitions
│   ├── api/
│   │   ├── main.py               # FastAPI app
│   │   ├── routers/
│   │   │   ├── bookings.py
│   │   │   ├── customers.py
│   │   │   ├── barbers.py
│   │   │   └── services.py
│   │   └── models.py             # Request/response models
│   ├── core/
│   │   ├── models.py             # SQLAlchemy ORM models
│   │   ├── database.py           # DB configuration
│   │   ├── business_rules.py     # Rule definitions
│   │   └── validators.py         # Input validation
│   └── utils/
│       ├── config.py             # Configuration
│       └── logging.py            # Setup
├── tests/
├── alembic/                      # Database migrations
├── docs/
├── chainlit.md                   # Chainlit config
├── run.py                        # Entry point
├── pyproject.toml
└── README.md
```

## Configuration

### Environment Variables
```env
OPENAI_API_KEY=your-key
DATABASE_URL=sqlite:///./bookings.db
# or postgresql://user:pass@localhost/barber
CHAINLIT_AUTH_PASSWORD=secure-password
```

### Business Rules Configuration
- 2-hour booking notice
- 24-hour cancellation deadline
- Service duration per barber
- Operating hours
- Pricing tiers

## Integration Points

1. **OpenAI API**: LLM backend
2. **Chainlit**: Conversational UI
3. **FastAPI**: REST API server
4. **SQLAlchemy**: ORM and database
5. **Alembic**: Database migrations
6. **LangGraph**: Workflow orchestration

## Use Cases

- AI-powered booking systems
- Customer service automation
- Business policy enforcement
- Human-in-the-loop workflows
- Production agent examples
- Middleware pattern demonstrations

## Best Practices Demonstrated

1. Clear middleware composition
2. Separation of concerns
3. Business logic in middleware
4. Human oversight for critical ops
5. Type safety with SQLAlchemy
6. Error handling and recovery
7. Comprehensive logging
8. API versioning
9. Database migrations
10. Configuration management

## Production Considerations

- Authentication and authorization
- Rate limiting on API
- Database connection pooling
- Async execution
- Error recovery
- Monitoring and alerts
- Logging and auditing
- Backup strategy
- Load testing
- Scaling approach

## Security Measures

- PII masking in logs
- Input validation
- SQL injection prevention via ORM
- API authentication
- CORS configuration
- Rate limiting
- Encrypted credentials
- Audit trails

## Observability

- Token usage tracking
- Conversation metrics
- Booking success rates
- Error tracking
- Response time monitoring
- Middleware performance
- Database query performance

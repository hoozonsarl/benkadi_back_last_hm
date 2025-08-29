# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Benkadi Blood is a FastAPI-based blood bank management system with PostgreSQL database, Redis caching, RabbitMQ message queuing, and Celery for background tasks. The application manages blood donors, recipients, blood samples, distributions, and hospital operations with comprehensive authentication and authorization.

## Architecture

### Core Stack
- **Backend**: FastAPI (Python 3.10)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: JWT tokens with OAuth2 bearer scheme
- **Caching**: Redis
- **Message Queue**: RabbitMQ
- **Background Tasks**: Celery with Flower monitoring
- **Database Migrations**: Alembic
- **Containerization**: Docker with Docker Compose

### Project Structure
```
├── app.py                 # FastAPI application entry point
├── main.py               # Development server runner
├── config/               # Configuration settings
├── database/             # Database setup and DAOs
│   ├── dao/             # Data Access Objects
│   └── database.py      # SQLAlchemy setup
├── models/              # SQLAlchemy models
├── routes/              # FastAPI route handlers
├── schemas/             # Pydantic schemas for API
├── auth/                # Authentication and authorization
├── service/             # Business logic services
│   └── sms/            # SMS/WhatsApp messaging
├── tasks.py             # Celery background tasks
├── tests/               # Test suite
├── static/              # Static files storage
└── alembic/             # Database migrations
```

### Key Components

#### Authentication System
- JWT-based authentication with OAuth2PasswordBearer
- Token handling in `auth/jwt_handler.py`
- User dependency injection in `auth/deps.py`
- Login endpoint: `/users/login`

#### Database Layer
- PostgreSQL connection configured in `database/database.py`
- DAO pattern implemented in `database/dao/` for each model
- Models define SQLAlchemy entities for blood management domain
- Connection URL format: `postgresql://user:pass@server:port/db`

#### Background Tasks
- Celery configuration in `tasks.py`
- Scheduled tasks for birthday messages and monthly reports
- WhatsApp messaging integration for donor communication
- Redis backend for task results, RabbitMQ for message broker

#### API Routes
Each domain has dedicated router:
- `/users` - User management and authentication
- `/donneurs` - Blood donor management
- `/receveurs` - Blood recipient management
- `/prelevements` - Blood collection/sampling
- `/poche-de-sangs` - Blood bag inventory
- `/distributions` - Blood distribution tracking
- `/hospitals` - Hospital management
- `/dashboards` - Analytics and reporting

## Development Commands

### Docker Development (Recommended)
```bash
# Start all services
docker-compose up

# Start in background
docker-compose up -d

# View logs
docker-compose logs -f app

# Stop services
docker-compose down
```

### Database Operations
```bash
# Create new migration
docker-compose exec app alembic revision --autogenerate -m "migration description"

# Apply migrations
docker-compose exec app alembic upgrade head

# Downgrade migration
docker-compose exec app alembic downgrade -1
```

### Local Development (Alternative)
```bash
# Install dependencies
pip install -r requirements.txt

# Run development server
python main.py

# Run with uvicorn directly
uvicorn app:app --host 0.0.0.0 --port 8080 --reload
```

### Testing
```bash
# Run tests (in container)
docker-compose exec app pytest

# Run specific test file
docker-compose exec app pytest tests/test_users.py

# Run tests locally
pytest
```

### Celery Operations
```bash
# Monitor tasks with Flower
# Access: http://localhost:5555
# Credentials: samanidarix@gmail.com:6775212952

# Manual task execution (in container)
docker-compose exec app python -c "from tasks import scheduled_sms_task; scheduled_sms_task.delay('phone', 'message')"
```

## Configuration

### Environment Variables
Set in docker-compose.yml or .env file:
- `POSTGRES_USER=darix`
- `POSTGRES_PASSWORD=darix` 
- `POSTGRES_DB=benkadi_blood`
- `POSTGRES_SERVER=db` (container name)
- `PYTHONPATH=/app`

### Service Ports
- API: http://localhost:8081 (exposed from container port 8080)
- API Docs: http://localhost:8081/docs
- PostgreSQL: localhost:8001
- PgAdmin: http://localhost:5050
- Redis: localhost:6379
- RabbitMQ Management: http://localhost:15672
- Flower (Celery): http://localhost:5555

## Code Conventions

### Database Access
- Always use DAO pattern from `database/dao/` directory
- Get database session via `get_db()` dependency
- Close sessions properly in finally blocks

### API Endpoints
- Use appropriate HTTP methods (GET, POST, PUT, DELETE)
- Include proper Pydantic schemas for request/response validation
- Add authentication dependency where required: `Depends(get_current_user)`
- Group routes by domain using APIRouter with consistent prefixes

### Error Handling
- Use FastAPI HTTPException for API errors
- Include appropriate status codes and descriptive messages
- Log errors appropriately for debugging

### Background Tasks
- Use Celery tasks for long-running operations
- Configure retry policies with `autoretry_for` and `retry_backoff`
- Use database sessions within task context managers

## Testing Strategy

- Test client configured in `tests/setup.py`
- Uses same database as development (consider test-specific DB)
- FastAPI TestClient for endpoint testing
- Override dependencies for testing isolation

## Blood Management Domain

This system manages:
- **Donors (Donneurs)**: People who donate blood
- **Recipients (Receveurs)**: Patients receiving blood
- **Blood Samples (Prelevements)**: Collection events
- **Blood Bags (Poches de Sangs)**: Storage units
- **Fractions**: Blood components (plasma, platelets, etc.)
- **Distributions**: Blood allocation to hospitals
- **Hospitals**: Healthcare facilities
- **Users**: System operators with role-based permissions

## Key Business Logic

### Automated Communications
- Birthday messages sent to donors via WhatsApp
- SMS/WhatsApp integration for notifications
- Monthly reporting with data visualization

### Permission System
- Role-based access control
- User groups with granular permissions
- JWT token validation on protected endpoints

### Data Integrity
- Foreign key relationships between entities
- Audit logging for critical operations
- Proper validation through Pydantic schemas
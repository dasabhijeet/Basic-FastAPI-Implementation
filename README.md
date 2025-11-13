# Admin Portal API - FastAPI Implementation

A production-ready FastAPI application with async MySQL, designed for building admin portal APIs. Features a clean, maintainable architecture that follows industry best practices.

## Features

- ✅ **Async Database**: aiomysql with connection pooling
- ✅ **Clean Architecture**: Layered structure (routers → services → database)
- ✅ **Multi-Environment**: Separate configs for dev, test, and prod
- ✅ **Docker Support**: Full containerization with docker-compose
- ✅ **Database Migrations**: SQL-based migration system
- ✅ **Comprehensive Logging**: Structured JSON logging
- ✅ **Global Error Handling**: Consistent error responses
- ✅ **API Documentation**: Auto-generated Swagger/ReDoc docs
- ✅ **Testing Framework**: Pytest with async support
- ✅ **Type Safety**: Full type hints with Pydantic validation
- ✅ **Security Ready**: Password hashing, JWT placeholders

## Project Structure

```
Basic-FastAPI-Implementation/
├── app/
│   ├── core/              # Configuration and settings
│   │   ├── config.py      # Environment-based settings
│   │   ├── dependencies.py# Dependency injection
│   │   ├── logging.py     # Logging configuration
│   │   └── security.py    # Security utilities
│   ├── db/                # Database layer
│   │   ├── database.py    # Async connection pool
│   │   ├── base.py        # Base DB operations
│   │   └── models.py      # Table definitions
│   ├── routers/           # API endpoints
│   │   ├── users.py       # User CRUD endpoints
│   │   └── health.py      # Health check
│   ├── schemas/           # Pydantic models
│   │   ├── user_schema.py # User validation models
│   │   └── common_schema.py# Shared schemas
│   ├── services/          # Business logic
│   │   └── user_service.py# User service layer
│   ├── middlewares/       # Custom middleware
│   │   ├── error_handler.py
│   │   ├── logging_middleware.py
│   │   └── cors_middleware.py
│   └── main.py            # Application entry point
├── migrations/            # SQL migrations
├── scripts/               # Utility scripts
├── tests/                 # Test suite
├── .env.dev              # Development config
├── .env.test             # Test config
├── .env.prod             # Production config
├── docker-compose.yml    # Docker services
├── Dockerfile            # App container
└── requirements.txt      # Python dependencies
```

## Quick Start

### Prerequisites

- Python 3.11+
- MySQL 8.0+
- Docker & Docker Compose (optional)

### Option 1: Local Development

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd Basic-FastAPI-Implementation
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env.dev
   # Edit .env.dev with your database credentials
   ```

5. **Initialize database**
   ```bash
   python scripts/init_db.py
   ```

6. **Run the application**
   ```bash
   # Set environment
   export ENVIRONMENT=dev  # On Windows: set ENVIRONMENT=dev

   # Start server
   uvicorn app.main:app --reload
   ```

7. **Access the API**
   - API Documentation: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc
   - Health Check: http://localhost:8000/api/v1/health

### Option 2: Docker (Recommended)

1. **Clone and configure**
   ```bash
   git clone <your-repo-url>
   cd Basic-FastAPI-Implementation
   cp .env.example .env.dev
   ```

2. **Start services**
   ```bash
   docker-compose up -d
   ```

3. **Access the API**
   - API: http://localhost:8000
   - Docs: http://localhost:8000/docs
   - phpMyAdmin: http://localhost:8080 (with `--profile dev`)

## Environment Configuration

### Multiple Environments

The application supports three environments:

- **Development** (`.env.dev`): Debug mode, verbose logging
- **Test** (`.env.test`): Test database, test-specific settings
- **Production** (`.env.prod`): Optimized for production

### Switching Environments

```bash
# Set environment variable
export ENVIRONMENT=prod

# Or use it directly
ENVIRONMENT=prod uvicorn app.main:app
```

### Key Configuration Options

```env
# Application
APP_NAME=Admin Portal API
DEBUG=true
ENVIRONMENT=dev

# Database
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=admin_portal_dev

# Server
HOST=0.0.0.0
PORT=8000
RELOAD=true

# Logging
LOG_LEVEL=DEBUG
LOG_FORMAT=text  # or json
```

## API Endpoints

### User Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/users` | List all users (paginated) |
| GET | `/api/v1/users/{id}` | Get user by ID |
| POST | `/api/v1/users` | Create new user |
| PUT | `/api/v1/users/{id}` | Update user |
| DELETE | `/api/v1/users/{id}` | Delete user |
| GET | `/api/v1/users/search?q=term` | Search users by name |

### Health Check

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/health` | Service health status |

## Database Management

### Running Migrations

```bash
# Run all pending migrations
python scripts/run_migrations.py

# Or initialize fresh database
python scripts/init_db.py
```

### Creating New Migrations

1. Create new file: `migrations/00X_description.sql`
2. Write your SQL DDL statements
3. Run migrations: `python scripts/run_migrations.py`

### Example Migration

```sql
-- migrations/002_add_products_table.sql
CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    price DECIMAL(10, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;
```

## Testing

### Run Tests

```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_api/test_users.py
```

### Writing Tests

```python
# tests/test_api/test_users.py
async def test_get_users(client):
    response = await client.get("/api/v1/users")
    assert response.status_code == 200
    assert "data" in response.json()
```

## Development Workflow

### Adding a New Endpoint

1. **Create schema** (`app/schemas/product_schema.py`)
2. **Define model** (add to `app/db/models.py`)
3. **Create service** (`app/services/product_service.py`)
4. **Add router** (`app/routers/products.py`)
5. **Register in main.py**
6. **Create migration** (`migrations/00X_products.sql`)
7. **Write tests** (`tests/test_api/test_products.py`)

### Code Quality

```bash
# Format code
black app tests

# Sort imports
isort app tests

# Type checking
mypy app

# Linting
flake8 app
```

## Deployment

### Production Checklist

- [ ] Update `.env.prod` with real credentials
- [ ] Generate strong `SECRET_KEY`
- [ ] Set `DEBUG=false`
- [ ] Configure production database
- [ ] Update `CORS_ORIGINS` with actual domains
- [ ] Set up SSL/TLS certificates
- [ ] Configure reverse proxy (Nginx)
- [ ] Set up monitoring and logging
- [ ] Backup database regularly

### Docker Production Deployment

```bash
# Build production image
docker build -t admin-portal-api:latest .

# Run with production env
ENVIRONMENT=prod docker-compose up -d
```

## Troubleshooting

### Database Connection Issues

```bash
# Check MySQL is running
docker-compose ps

# View logs
docker-compose logs mysql

# Test connection
mysql -h localhost -u root -p
```

### Application Logs

```bash
# Docker logs
docker-compose logs api

# Local logs
# Logs are output to stdout
```

## Contributing

### For Junior Developers

This project follows a clear pattern for adding features:

1. **Schema**: Define request/response models
2. **Service**: Write business logic (SQL queries here)
3. **Router**: Create HTTP endpoints
4. **Test**: Write tests for your code

Example workflow documented in: `docs/ADDING_FEATURES.md`

## License

MIT License

## Support

For issues and questions:
- Create an issue in the repository
- Check existing documentation
- Review API documentation at `/docs`

---

**Version**: 1.0.0
**Last Updated**: 2025-01-13

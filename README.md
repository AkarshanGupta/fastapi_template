# FastAPI Template

A production-ready FastAPI backend project template with a modular, scalable structure. This template includes placeholders for many backend features, all controlled via feature flags for maximum flexibility.

## 🚀 Features

- **Modular Architecture**: Clean separation of concerns with routers, services, and models
- **Feature Flags**: All optional features can be enabled/disabled via environment variables
- **Production Safety**: Built-in validation to prevent unsafe configurations
- **Type Safety**: Full type hints using Pydantic and Python typing
- **Testing Ready**: Comprehensive test suite with pytest
- **Docker Support**: Production-ready Dockerfile and docker-compose setup
- **Lazy Loading**: Heavy dependencies are only imported when features are enabled

## 📁 Project Structure

```
fastapi_template/
├── app/
│   ├── main.py                 # Application factory with feature flags
│   ├── settings.py             # Pydantic BaseSettings + feature toggles
│   ├── dependencies.py         # Reusable dependency injection patterns
│   ├── logging_conf.py         # Production-safe logging configuration
│   ├── decorators.py           # Feature guard decorators
│   ├── routers/                # API route handlers
│   │   ├── health.py           # Health check endpoints
│   │   ├── items.py            # Demo CRUD endpoints (works without DB)
│   │   └── ocr.py              # OCR endpoints (requires ENABLE_OCR)
│   ├── services/               # Business logic and external integrations
│   │   ├── db_postgres.py      # PostgreSQL connector (placeholder)
│   │   ├── db_mongo.py         # MongoDB connector (placeholder)
│   │   ├── ocr_service.py      # OCR service abstraction
│   │   └── storage.py          # File storage service
│   ├── models/                 # SQLAlchemy models (placeholder)
│   └── tests/                  # Test suite
│       ├── test_health.py
│       ├── test_feature_flags.py
│       ├── test_cors.py
│       └── conftest.py
├── requirements.txt
├── .env.example
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## 🛠️ Installation

### Prerequisites

- Python 3.11+
- pip
- (Optional) Docker and Docker Compose

### Local Setup

1. **Clone or copy this template**:
   ```bash
   cd fastapi_template
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Copy environment file**:
   ```bash
   cp .env.example .env
   ```

5. **Configure your `.env` file** (see Configuration section below)

6. **Run the application**:
   ```bash
   uvicorn app.main:app --reload
   ```

The API will be available at `http://localhost:8000`

- API Documentation: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## ⚙️ Configuration

### Environment Variables

All configuration is done via environment variables. Copy `.env.example` to `.env` and customize:

#### Basic Settings

- `ENVIRONMENT`: `development`, `staging`, or `production`
- `DEBUG`: `True` or `False` (must be `False` in production)
- `CORS_ORIGINS`: Comma-separated list of allowed origins

#### Feature Flags

Enable/disable optional features:

- `ENABLE_DB_POSTGRES`: Enable PostgreSQL support
- `ENABLE_DB_MONGO`: Enable MongoDB support
- `ENABLE_OCR`: Enable OCR endpoints
- `ENABLE_STORAGE`: Enable file storage service

### Enabling Features

#### Enable PostgreSQL

1. Set `ENABLE_DB_POSTGRES=True` in `.env`
2. Configure PostgreSQL connection:
   ```
   POSTGRES_HOST=localhost
   POSTGRES_PORT=5432
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=your_password
   POSTGRES_DB=fastapi_db
   ```
3. Install PostgreSQL driver (uncomment in `requirements.txt`):
   ```bash
   pip install asyncpg
   ```

#### Enable MongoDB

1. Set `ENABLE_DB_MONGO=True` in `.env`
2. Configure MongoDB connection:
   ```
   MONGO_HOST=localhost
   MONGO_PORT=27017
   MONGO_DB=fastapi_db
   ```
3. Install MongoDB driver (uncomment in `requirements.txt`):
   ```bash
   pip install motor
   ```

#### Enable OCR

1. Set `ENABLE_OCR=True` in `.env`
2. Configure OCR provider:
   ```
   OCR_PROVIDER=tesseract  # or google_vision, aws_textract
   OCR_API_KEY=your_api_key  # if required
   ```
3. Install OCR libraries (uncomment in `requirements.txt`):
   ```bash
   pip install pytesseract Pillow
   ```

#### Enable Storage

1. Set `ENABLE_STORAGE=True` in `.env`
2. Configure storage type:
   ```
   STORAGE_TYPE=local  # or s3, gcs
   STORAGE_PATH=./storage
   ```
3. For S3/GCS, install additional libraries as needed

## 🐳 Docker Setup

### Using Docker Compose

1. **Start all services**:
   ```bash
   docker-compose up -d
   ```

2. **View logs**:
   ```bash
   docker-compose logs -f api
   ```

3. **Stop services**:
   ```bash
   docker-compose down
   ```

### Using Dockerfile

1. **Build image**:
   ```bash
   docker build -t fastapi_template .
   ```

2. **Run container**:
   ```bash
   docker run -p 8000:8000 --env-file .env fastapi_template
   ```

## 🧪 Testing

Run the test suite:

```bash
pytest
```

Run with coverage:

```bash
pytest --cov=app --cov-report=html
```

### Test Structure

- `test_health.py`: Tests health check endpoints
- `test_feature_flags.py`: Tests feature flag functionality
- `test_cors.py`: Tests CORS headers and preflight requests
- `conftest.py`: Shared fixtures and test configuration

## 📝 Adding New Modules

### Adding a New Router

1. Create a new file in `app/routers/`:
   ```python
   from fastapi import APIRouter
   
   router = APIRouter()
   
   @router.get("/example")
   async def example_endpoint():
       return {"message": "Hello"}
   ```

2. Mount it in `app/main.py`:
   ```python
   from app.routers import example
   
   app.include_router(example.router, prefix=settings.API_V1_PREFIX, tags=["example"])
   ```

### Adding a New Service

1. Create a new file in `app/services/`:
   ```python
   from app.settings import Settings
   
   async def init_service(settings: Settings):
       # Initialize service
       pass
   ```

2. Add feature flag in `app/settings.py`:
   ```python
   ENABLE_NEW_SERVICE: bool = False
   ```

3. Conditionally initialize in `app/main.py`:
   ```python
   if settings.ENABLE_NEW_SERVICE:
       from app.services.new_service import init_service
       # Initialize service
   ```

### Adding a New Feature Flag

1. Add flag to `app/settings.py`:
   ```python
   ENABLE_NEW_FEATURE: bool = False
   ```

2. Use in code with guard:
   ```python
   from app.decorators import feature_guard
   
   @router.get("/new-feature")
   async def new_feature(settings: Settings = Depends(get_settings)):
       feature_guard(settings, "ENABLE_NEW_FEATURE")
       # Feature logic
   ```

## 🔒 Production Safety

The template includes several production safety features:

1. **Debug Mode Validation**: If `ENVIRONMENT=production` and `DEBUG=True`, the application will fail to start
2. **Strict CORS**: In production, only configured origins are allowed
3. **No Docs in Production**: API documentation is disabled in production mode
4. **Non-root Docker User**: Dockerfile runs as non-root user for security

## 🔄 Template Evolution Workflow

This template is designed to evolve over multiple projects:

1. **Start Fresh**: Copy this template for each new project
2. **Enable Features**: Turn on only the features you need via feature flags
3. **Implement Placeholders**: Replace placeholder code with actual implementations
4. **Add New Features**: Add new modules following the established patterns
5. **Update Template**: As you discover improvements, update the base template
6. **Share Knowledge**: Document patterns and best practices

### Recommended Evolution Path

1. **Phase 1**: Start with minimal features (health, items endpoints)
2. **Phase 2**: Enable database as needed (PostgreSQL or MongoDB)
3. **Phase 3**: Add specialized services (OCR, storage) when required
4. **Phase 4**: Implement actual business logic in placeholders
5. **Phase 5**: Add authentication, authorization, and other advanced features

## 📚 API Endpoints

### Health Check

- `GET /api/v1/health` - Returns application status

### Items (Always Available)

- `GET /api/v1/items` - List all items
- `GET /api/v1/items/{id}` - Get item by ID
- `POST /api/v1/items` - Create new item
- `PUT /api/v1/items/{id}` - Update item
- `DELETE /api/v1/items/{id}` - Delete item

### OCR (Requires ENABLE_OCR=True)

- `GET /api/v1/ocr/status` - Get OCR service status
- `POST /api/v1/ocr/process` - Process OCR on uploaded image

## 🐛 Troubleshooting

### Feature Not Working

- Check that the feature flag is enabled in `.env`
- Verify required dependencies are installed
- Check application logs for errors

### Database Connection Issues

- Ensure database service is running
- Verify connection credentials in `.env`
- Check network connectivity (Docker networking)

### CORS Issues

- Verify `CORS_ORIGINS` includes your frontend URL
- Check that credentials are properly configured
- In production, ensure strict CORS settings

## 📄 License

This template is provided as-is for use in your projects.

## 🤝 Contributing

When improving this template:

1. Maintain backward compatibility with existing feature flags
2. Keep placeholder implementations simple and clear
3. Document new patterns in this README
4. Update tests for new features
5. Follow the existing code style and structure

## 📞 Support

For issues or questions:

1. Check the documentation above
2. Review example implementations in the code
3. Check test files for usage examples
4. Review logs for detailed error messages

---

**Happy Coding! 🚀**


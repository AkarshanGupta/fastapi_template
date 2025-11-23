"""
FastAPI application factory with feature flags.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.settings import Settings
from app.logging_conf import setup_logging
from app.routers import health, items, ocr


def create_app(settings: Settings = None) -> FastAPI:
    """
    Create and configure FastAPI application.
    
    Args:
        settings: Application settings. If None, creates a new instance.
        
    Returns:
        Configured FastAPI application
    """
    if settings is None:
        settings = Settings()
    
    # Setup logging
    setup_logging(settings)
    
    # Create FastAPI app
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        debug=settings.DEBUG,
        docs_url="/docs" if not settings.is_production else None,
        redoc_url="/redoc" if not settings.is_production else None,
    )
    
    # Configure CORS
    _configure_cors(app, settings)
    
    # Mount routers (always available)
    app.include_router(health.router, prefix=settings.API_V1_PREFIX, tags=["health"])
    app.include_router(items.router, prefix=settings.API_V1_PREFIX, tags=["items"])
    
    # Conditionally mount feature-specific routers
    if settings.ENABLE_OCR:
        app.include_router(ocr.router, prefix=settings.API_V1_PREFIX, tags=["ocr"])
    
    # Initialize optional services (lazy loading)
    if settings.ENABLE_DB_POSTGRES:
        _init_postgres(app, settings)
    
    if settings.ENABLE_DB_MONGO:
        _init_mongo(app, settings)
    
    if settings.ENABLE_STORAGE:
        _init_storage(app, settings)
    
    return app


def _configure_cors(app: FastAPI, settings: Settings) -> None:
    """
    Configure CORS middleware.
    
    Args:
        app: FastAPI application
        settings: Application settings
    """
    # In production, use strict CORS
    if settings.is_production:
        allowed_origins = settings.CORS_ORIGINS
    else:
        # In development, allow all origins if CORS_ORIGINS is empty
        allowed_origins = settings.CORS_ORIGINS if settings.CORS_ORIGINS else ["*"]
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
        allow_methods=settings.CORS_ALLOW_METHODS,
        allow_headers=settings.CORS_ALLOW_HEADERS,
    )


def _init_postgres(app: FastAPI, settings: Settings) -> None:
    """
    Initialize PostgreSQL connection (lazy import).
    
    Args:
        app: FastAPI application
        settings: Application settings
    """
    try:
        from app.services.db_postgres import init_postgres_db
        
        @app.on_event("startup")
        async def startup_postgres():
            await init_postgres_db(settings)
        
        @app.on_event("shutdown")
        async def shutdown_postgres():
            from app.services.db_postgres import close_postgres_db
            await close_postgres_db()
    except ImportError:
        # If psycopg2 or asyncpg not installed, skip
        pass


def _init_mongo(app: FastAPI, settings: Settings) -> None:
    """
    Initialize MongoDB connection (lazy import).
    
    Args:
        app: FastAPI application
        settings: Application settings
    """
    try:
        from app.services.db_mongo import init_mongo_db
        
        @app.on_event("startup")
        async def startup_mongo():
            await init_mongo_db(settings)
        
        @app.on_event("shutdown")
        async def shutdown_mongo():
            from app.services.db_mongo import close_mongo_db
            await close_mongo_db()
    except ImportError:
        # If motor or pymongo not installed, skip
        pass


def _init_storage(app: FastAPI, settings: Settings) -> None:
    """
    Initialize storage service (lazy import).
    
    Args:
        app: FastAPI application
        settings: Application settings
    """
    try:
        from app.services.storage import init_storage_service
        
        @app.on_event("startup")
        async def startup_storage():
            await init_storage_service(settings)
    except ImportError:
        # If storage libraries not installed, skip
        pass


# Create app instance (for uvicorn)
app = create_app()



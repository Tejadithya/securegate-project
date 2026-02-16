from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from .database import engine, Base
from .routes.auth_routes import router as auth_router
from .routes.admin_routes import router as admin_router
from .routes.resource_routes import router as resource_router
from .middleware import AuthorizationMiddleware
import logging

logger = logging.getLogger(__name__)

# Create database tables on startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Database connection error: {e}")
        logger.info("Make sure PostgreSQL is running and credentials are correct")
        logger.info("Database URL should be: postgresql://postgres:PASSWORD@localhost:5432/progres")
    yield

app = FastAPI(title="SecureGate RBAC System", lifespan=lifespan)

# Add custom authorization middleware
app.add_middleware(AuthorizationMiddleware)

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8000", "file://"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(admin_router, prefix="/admin", tags=["Administration"])
app.include_router(resource_router, prefix="/resource", tags=["Resources"])

@app.get("/")
def read_root():
    return {"message": "Welcome to SecureGate RBAC System"}

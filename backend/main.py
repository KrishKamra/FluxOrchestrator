from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer
from .routes import auth, datasets, jobs

# This tells FastAPI where the login logic resides
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Define the Security Schema for Swagger UI
# This is the "Magic" that makes the global lock appear
app = FastAPI(
    title="Mini AI SaaS Platform",
    description="Industry-grade AI Training & Management System",
    version="2.0.0",
    swagger_ui_parameters={"persistAuthorization": True} # Optional: Keeps you logged in on refresh
)

# --- GLOBAL SECURITY CONFIG ---
# This ensures Swagger knows how to handle the Bearer Token
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.openapi.utils import get_openapi

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    # Add Security Schemes to the OpenAPI Schema
    openapi_schema["components"]["securitySchemes"] = {
        "OAuth2PasswordBearer": {
            "type": "oauth2",
            "flows": {
                "password": {
                    "tokenUrl": "auth/login",
                    "scopes": {}
                }
            }
        }
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# --- ENDPOINTS ---

@app.get("/")
def read_root():
    return {
        "status": "Online",
        "message": "Welcome to the Modular AI SaaS Platform!",
        "version": "2.0.0"
    }

# Include Routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(datasets.router, prefix="/datasets", tags=["Datasets"])
app.include_router(jobs.router, prefix="/jobs", tags=["Training Jobs"])
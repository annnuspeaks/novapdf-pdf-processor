from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from starlette.responses import Response

from app.api.routes import router
from app.config import settings
from app.request_limits import RequestSizeLimitMiddleware

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Free online PDF tools API.",
    debug=settings.debug,
)

app.add_middleware(
    RequestSizeLimitMiddleware,
    max_body_size=100 * 1024 * 1024,
)

# --------------------------------------------------
# Custom OpenAPI Schema
# --------------------------------------------------


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    schema["openapi"] = "3.0.3"

    components = schema.get("components", {}).get("schemas", {})

    for schema_data in components.values():
        properties = schema_data.get("properties", {})

        for property_data in properties.values():

            # Multiple uploaded files
            if (
                property_data.get("type") == "array"
                and isinstance(property_data.get("items"), dict)
            ):
                items = property_data["items"]

                if items.get("contentMediaType"):
                    items.pop("contentMediaType", None)
                    items["type"] = "string"
                    items["format"] = "binary"

            # Single uploaded file
            if (
                property_data.get("type") == "string"
                and property_data.get("contentMediaType")
            ):
                property_data.pop("contentMediaType", None)
                property_data["format"] = "binary"

    app.openapi_schema = schema
    return app.openapi_schema


app.openapi = custom_openapi

# --------------------------------------------------
# CORS Configuration
# --------------------------------------------------

origins = [
    origin.strip()
    for origin in settings.frontend_origins.split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)

# --------------------------------------------------
# Security Headers Middleware
# --------------------------------------------------


@app.middleware("http")
async def add_security_headers(
    request: Request,
    call_next,
) -> Response:
    response = await call_next(request)

    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "no-referrer"

    # PDF and extracted-text responses may contain user documents.
    # Prevent browsers and intermediaries from caching API responses.
    if request.url.path.startswith("/api/"):
        response.headers["Cache-Control"] = "no-store"

    return response

# --------------------------------------------------
# API Routes
# --------------------------------------------------


app.include_router(router)

# --------------------------------------------------
# Root Endpoint
# --------------------------------------------------


@app.get("/", tags=["Root"])
async def root() -> dict[str, str]:
    return {
        "message": "Welcome to NOVA PDF API",
        "docs": "/docs",
    }

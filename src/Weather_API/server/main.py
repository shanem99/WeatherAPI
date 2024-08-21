from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.encoders import jsonable_encoder
from Weather_API.server.api.core import api_router
import uvicorn
from starlette.middleware.cors import CORSMiddleware
from Weather_API.db.sqllite import lifespan


app = FastAPI(
    default_response_class=JSONResponse,
    title="Weather API",
    description="API for weather data",
    version="0.0.1",
    lifespan=lifespan,
)


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        content=jsonable_encoder({"status": "ERROR", "detail": exc.detail}),
        status_code=exc.status_code,
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        content=jsonable_encoder({"status": "ERROR", "detail": exc.errors()}),
        status_code=400,
    )


app.include_router(api_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["Authorization", "Content-Type"],
    expose_headers=["Content-Type", "ETag", "Last-Modified"],
)

from fastapi import Depends, routing
from Weather_API.server.api.routers import OculaWeather

api_router = routing.APIRouter()

api_router.include_router(OculaWeather.router, tags=["Ocula Weather Data Task"])

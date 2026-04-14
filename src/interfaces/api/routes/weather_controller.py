from fastapi import APIRouter, Depends, HTTPException, status, Query
from src.application.services.weather_service import WeatherService
from src.interfaces.api.schemas.weather_schema import WeatherResponse
from src.interfaces.api.dependencies import get_weather_service

router = APIRouter(prefix="/external/weather", tags=["External Weather"])


@router.get("/current", response_model=WeatherResponse)
async def get_current_weather(
        city: str = Query(..., min_length=2, description="City name"),
        units: str = Query("metric", pattern="^(metric|imperial)$"),
        service: WeatherService = Depends(get_weather_service)
):
    weather = await service.get_current_weather(city, units)

    if not weather:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Weather data for '{city}' not found"
        )

    return WeatherResponse.model_validate(weather)

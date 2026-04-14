from pydantic import BaseModel, Field


class WeatherResponse(BaseModel):
    city: str
    temperature: float = Field(..., description="Temperature in selected units")
    feels_like: float = Field(..., description="Feels like temperature")
    humidity: float = Field(..., ge=0, le=100, description="Humidity percentage")
    description: str = Field(..., max_length=255)
    wind_speed: float = Field(..., ge=0, description="Wind speed")
    units: str = Field(..., pattern="^(metric|imperial)$")

    model_config = {"from_attributes": True}

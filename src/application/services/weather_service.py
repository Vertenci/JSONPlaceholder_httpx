import logging
from src.infrastructure.external_apis.openweather_client import OpenWeatherClient
from src.application.dtos.weather_dto import WeatherResponseDTO


logger = logging.getLogger(__name__)


class WeatherService:
    def __init__(self, weather_client: OpenWeatherClient):
        self.weather_client = weather_client

    async def get_current_weather(self, city: str, units: str = "metric") -> WeatherResponseDTO | None:
        logger.info(f"Getting weather for city: {city}")

        weather_data = await self.weather_client.get_current_weather(city, units)

        if not weather_data:
            return None

        return WeatherResponseDTO(
            city=weather_data.get("name"),
            temperature=weather_data.get("main", {}).get("temp", 0),
            feels_like=weather_data.get("main", {}).get("feels_like", 0),
            humidity=weather_data.get("main", {}).get("humidity", 0),
            description=weather_data.get("weather", [{}])[0].get("description", ""),
            wind_speed=weather_data.get("wind", {}).get("speed", 0),
            units=units
        )

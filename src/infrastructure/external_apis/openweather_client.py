import logging
from typing import Any
from .http_client import HTTPClient
from ..config.settings import settings

logger = logging.getLogger(__name__)


class OpenWeatherClient:
    def __init__(self, http_client: HTTPClient):
        self.http_client = http_client
        self.api_key = settings.OPENWEATHER_API_KEY

    async def get_current_weather(self, city: str, units: str = "metric") -> dict[str, Any] | None:
        logger.info(f"Fetching weather for city: {city}")

        try:
            return await self.http_client.get("/weather", params={
                "q": city,
                "appid": self.api_key,
                "units": units,
            })
        except Exception as e:
            logger.error(f"Failed to get weather for {city}: {e}")
            return None

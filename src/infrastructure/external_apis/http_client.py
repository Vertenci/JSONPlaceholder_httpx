import logging
from typing import Any, Self
import httpx

logger = logging.getLogger(__name__)


class HTTPClient:
    def __init__(self, base_url: str = ""):
        self.base_url = base_url
        self._client: httpx.AsyncClient | None = None

    async def __aenter__(self) -> Self:
        await self.initialize()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.close()

    async def initialize(self):
        if not self.base_url:
            logger.error("Cannot initialize HTTPClient: base_url is empty!")
            raise ValueError("base_url cannot be empty")

        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=httpx.Timeout(10.0),
            limits=httpx.Limits(max_keepalive_connections=20),
        )
        logger.info(f"HTTP Client initialized for {self.base_url}")

    async def close(self):
        if self._client:
            await self._client.aclose()
            logger.info("HTTP Client closed")

    async def get(self, endpoint: str, params: dict | None = None) -> Any:
        if not self._client:
            raise RuntimeError("HTTPClient not initialized. Use 'async with' context manager.")

        logger.debug(f"GET {endpoint} params={params}")
        try:
            response = await self._client.get(endpoint, params=params)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP {e.response.status_code} for {endpoint}")
            raise
        except httpx.RequestError as e:
            logger.error(f"Request failed: {e}")
            raise

    async def post(self, endpoint: str, data: dict | None = None, json: dict | None = None) -> dict[str, Any]:
        if not self._client:
            raise RuntimeError("HTTPClient not initialized. Use 'async with' context manager.")

        logger.debug(f"POST {endpoint} data={data} json={json}")
        try:
            if json is not None:
                response = await self._client.post(endpoint, json=json)
            else:
                response = await self._client.post(endpoint, data=data)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP {e.response.status_code} for {endpoint}")
            raise
        except httpx.RequestError as e:
            logger.error(f"Request failed: {e}")
            raise

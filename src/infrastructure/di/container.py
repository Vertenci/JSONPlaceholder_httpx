from typing import Self, Callable
from src.infrastructure.config.settings import settings
from src.infrastructure.database.database import db_manager
from src.infrastructure.database.unit_of_work import SqlAlchemyUnitOfWork
from src.infrastructure.external_apis.http_client import HTTPClient
from src.infrastructure.external_apis.jsonplaceholder_client import JSONPlaceholderClient
from src.infrastructure.external_apis.openweather_client import OpenWeatherClient
from src.application.services.user_service import UserService
from src.application.services.profile_service import ProfileService
from src.application.services.external_post_service import ExternalPostService
from src.application.services.weather_service import WeatherService
from src.domain.interfaces.unit_of_work import UnitOfWork


class DIContainer:
    def __init__(self):
        self._jsonplaceholder_http: HTTPClient | None = None
        self._openweather_http: HTTPClient | None = None

        self._jsonplaceholder_client: JSONPlaceholderClient | None = None
        self._openweather_client: OpenWeatherClient | None = None

        self._weather_service: WeatherService | None = None
        self._external_post_service: ExternalPostService | None = None

    async def __aenter__(self) -> Self:
        await self.initialize()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.close()

    async def initialize(self):
        await db_manager.initialize()

        self._jsonplaceholder_http = HTTPClient(base_url=settings.JSONPLACEHOLDER_API_URL)
        await self._jsonplaceholder_http.initialize()

        self._openweather_http = HTTPClient(base_url=settings.OPENWEATHER_API_URL)
        await self._openweather_http.initialize()

        self._jsonplaceholder_client = JSONPlaceholderClient(self._jsonplaceholder_http)
        self._openweather_client = OpenWeatherClient(self._openweather_http)

        self._weather_service = WeatherService(self._openweather_client)
        self._external_post_service = ExternalPostService(self._jsonplaceholder_client)

    async def close(self):
        if self._jsonplaceholder_http:
            await self._jsonplaceholder_http.close()
        if self._openweather_http:
            await self._openweather_http.close()

        await db_manager.close()

    def _get_uow_factory(self) -> Callable[[], UnitOfWork]:
        def factory() -> UnitOfWork:
            session_factory = db_manager.get_session_factory()
            return SqlAlchemyUnitOfWork(session_factory)

        return factory

    async def get_user_service(self) -> UserService:
        uow_factory = self._get_uow_factory()
        return UserService(uow_factory, self._jsonplaceholder_client)

    async def get_profile_service(self) -> ProfileService:
        uow_factory = self._get_uow_factory()
        return ProfileService(uow_factory)

    async def get_weather_service(self) -> WeatherService:
        if not self._weather_service:
            raise RuntimeError("Container not initialized. Call initialize() first.")
        return self._weather_service

    async def get_external_post_service(self) -> ExternalPostService:
        if not self._external_post_service:
            raise RuntimeError("Container not initialized. Call initialize() first.")
        return self._external_post_service


_container: DIContainer | None = None


def get_container() -> DIContainer:
    global _container
    if _container is None:
        _container = DIContainer()
    return _container

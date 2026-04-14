from fastapi import Depends
from src.application.services.external_post_service import ExternalPostService
from src.application.services.profile_service import ProfileService
from src.application.services.user_service import UserService
from src.application.services.weather_service import WeatherService
from src.infrastructure.di.container import get_container


async def get_user_service() -> UserService:
    container = get_container()
    return await container.get_user_service()


async def get_profile_service() -> ProfileService:
    container = get_container()
    return await container.get_profile_service()


async def get_external_post_service() -> ExternalPostService:
    container = get_container()
    return await container.get_external_post_service()


async def get_weather_service() -> WeatherService:
    container = get_container()
    return await container.get_weather_service()

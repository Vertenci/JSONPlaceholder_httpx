import logging
from typing import Optional, Any
from functools import wraps
from src.infrastructure.cache.redis_client import redis_client
from src.infrastructure.config.settings import settings

logger = logging.getLogger(__name__)


class CacheService:
    """Сервис для работы с кешем"""

    @staticmethod
    async def get_user(user_id: int) -> Optional[dict]:
        """Получение пользователя из кеша"""
        key = f"user:{user_id}"
        return await redis_client.get(key)

    @staticmethod
    async def set_user(user_id: int, user_data: dict) -> bool:
        """Сохранение пользователя в кеш"""
        key = f"user:{user_id}"
        return await redis_client.set(key, user_data, settings.CACHE_USER_TTL)

    @staticmethod
    async def invalidate_user(user_id: int) -> bool:
        """Инвалидация кеша пользователя"""
        keys = [
            f"user:{user_id}",
            f"profile:{user_id}",
        ]
        deleted = await redis_client.delete(*keys)
        # Также удаляем все списки пользователей
        await redis_client.delete_pattern("users:list:*")
        return deleted > 0

    @staticmethod
    async def get_profile(user_id: int) -> Optional[dict]:
        """Получение профиля из кеша"""
        key = f"profile:{user_id}"
        return await redis_client.get(key)

    @staticmethod
    async def set_profile(user_id: int, profile_data: dict) -> bool:
        """Сохранение профиля в кеш"""
        key = f"profile:{user_id}"
        return await redis_client.set(key, profile_data, settings.CACHE_PROFILE_TTL)

    @staticmethod
    async def invalidate_profile(user_id: int) -> bool:
        """Инвалидация кеша профиля"""
        key = f"profile:{user_id}"
        return await redis_client.delete(key) > 0


def cached(ttl: int = None, key_prefix: str = "cache"):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            cache_key = f"{key_prefix}:{func.__name__}:"

            if args:
                cache_key += ":".join(str(arg) for arg in args)
            if kwargs:
                cache_key += ":" + ":".join(f"{k}={v}" for k, v in sorted(kwargs.items()))

            cached_value = await redis_client.get(cache_key)
            if cached_value is not None:
                logger.debug(f"Cache hit for {cache_key}")
                return cached_value

            result = await func(*args, **kwargs)

            if result is not None:
                await redis_client.set(cache_key, result, ttl or settings.CACHE_DEFAULT_TTL)

            return result
        return wrapper
    return decorator


cache_service = CacheService()

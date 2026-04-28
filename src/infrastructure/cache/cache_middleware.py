import hashlib
import logging
from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from src.infrastructure.cache.redis_client import redis_client
from src.infrastructure.config.settings import settings

logger = logging.getLogger(__name__)

class CacheMiddleware(BaseHTTPMiddleware):
    def __init__(
            self,
            app,
            cacheable_path: list[str] | None = None,
            cacheable_methods: list[str] | None = None,
    ):
        super().__init__(app)
        self.cacheable_path = cacheable_path or [
            "/api/users",
            "/api/profiles",
            "/api/posts",
        ]
        self.cacheable_methods = cacheable_methods or ["GET"]
        self._path_patterns = self._compile_patterns()

    def _compile_patterns(self) -> list[tuple[str, bool]]:
        patterns = []
        for path in self.cacheable_path:
            is_pattern = "*" in path or "{" in path
            patterns.append((path, is_pattern))
        return patterns

    def _should_cache(self, request: Request) -> bool:
        if request.method not in self.cacheable_methods:
            return False

        if request.headers.get("Cache-Control") == "no-cache":
            return False

        path = request.url.path
        for pattern, is_pattern in self._path_patterns:
            if is_pattern:
                if self._match_pattern(path, pattern):
                    return True
            elif path.startswith(pattern):
                return True
        return False

    def _match_pattern(self, path: str, pattern: str) -> bool:
        import re
        regex_pattern = pattern.replace("{", "(?P<").replace("}", ">[^/]+)")
        regex_pattern = f"^{regex_pattern}$"
        return bool(re.match(regex_pattern, path))

    def _generate_cache_key(self, request: Request) -> str:
        key_parts = [
            request.method,
            request.url.path,
            str(sorted(request.query_params.items())),
        ]

        key_string = "|".join(key_parts)
        key_hash = hashlib.md5(key_string.encode()).hexdigest()

        return f"cache:http:{key_hash}"

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        if not self._should_cache(request):
            return await call_next(request)

        cache_key = self._generate_cache_key(request)

        try:
            cached_response = await redis_client.get(cache_key)
            if cached_response:
                logger.debug(f"Cache hit for {cache_key}")
                return Response(
                    content=cached_response["content"],
                    status_code=cached_response["status_code"],
                    headers=cached_response["headers"],
                    media_type=cached_response["media_type"],
                )
        except Exception as e:
            logger.error(f"Cache read error: {e}")

        response = await call_next(request)

        if response.status_code == 200:
            try:
                body = b""
                async for chunk in response.body_iterator:
                    body += chunk

                response_data = {
                    "content": body.decode("utf-8"),
                    "status_code": response.status_code,
                    "headers": dict(response.headers),
                    "media_type": response.media_type,
                }

                ttl = self._get_ttl_for_path(request.url.path)
                await redis_client.set(cache_key, response_data, ttl)

                return Response(
                    content=body,
                    status_code=response.status_code,
                    headers=dict(response.headers),
                    media_type=response.media_type,
                )
            except Exception as e:
                logger.error(f"Cache write error: {e}")
                return response

        return response

    def _get_ttl_for_path(self, path: str) -> int:
        if "/users" in path:
            return settings.CACHE_USER_TTL
        elif "/profiles" in path:
            return settings.CACHE_PROFILE_TTL
        return settings.CACHE_DEFAULT_TTL

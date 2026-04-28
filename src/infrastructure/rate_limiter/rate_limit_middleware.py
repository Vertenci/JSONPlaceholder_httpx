import logging
from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from src.infrastructure.rate_limiter.rate_limiter import rate_limiter

logger = logging.getLogger(__name__)


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(
            self,
            app,
            exclude_paths: list[str] | None = None,
    ):
        super().__init__(app)
        self.exclude_paths = exclude_paths or ["/health", "/metrics", "/docs", "/openapi.json"]

    def _should_limit(self, request: Request) -> bool:
        path = request.url.path
        for exclude_path in self.exclude_paths:
            if path.startswith(exclude_path):
                return False
        return True

    def _get_client_key(self, request: Request) -> str:
        api_key = request.headers.get("X-API-Key")
        if api_key:
            return f"apikey:{api_key}"

        if hasattr(request.state, "user_id"):
            return f"user:{request.state.user_id}"

        client_ip = self._get_client_ip(request)
        return f"ip:{client_ip}"

    def _get_client_ip(self, request: Request) -> str:
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            return forwarded.split(",")[0].strip()

        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip

        if request.client:
            return request.client.host

        return "unknown"

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        if not self._should_limit(request):
            return await call_next(request)

        client_key = self._get_client_key(request)

        is_allowed, headers = await rate_limiter.is_allowed(client_key)

        if not is_allowed:
            logger.warning(f"Rate limit exceeded for {client_key}")
            return Response(
                content='{"error": "Rate limit exceeded. Please try again later."}',
                status_code=429,
                headers=headers,
                media_type="application/json",
            )

        response = await call_next(request)

        for key, value in headers.items():
            response.headers[key] = value

        return response

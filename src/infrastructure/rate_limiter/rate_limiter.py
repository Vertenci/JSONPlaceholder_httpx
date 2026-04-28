import time
import logging
from src.infrastructure.cache.redis_client import redis_client
from src.infrastructure.config.settings import settings

logger = logging.getLogger(__name__)


class RateLimiter:
    def __init__(self):
        self.requests_limit = settings.RATE_LIMIT_REQUESTS
        self.period = settings.RATE_LIMIT_PERIOD
        self.burst_limit = settings.RATE_LIMIT_BURST

    async def is_allowed(
            self,
            key: str,
            cost: int = 1
    ) -> tuple[bool, dict]:
        now = time.time()
        window_start = now - self.period

        redis_key = f"rate_limit:{key}"

        try:
            async with redis_client._redis.pipeline() as pipe:
                await pipe.zremrangebyscore(redis_key, 0, window_start)

                await pipe.zcard(redis_key)

                await pipe.zadd(redis_key, {str(now): now})

                await pipe.expire(redis_key, self.period + 1)

                _, current_count, _, _ = await pipe.execute()

            is_allowed = current_count < self.requests_limit

            if cost > 1:
                burst_check = current_count + cost <= self.burst_limit
                is_allowed = is_allowed and burst_check

            remaining = max(0, self.requests_limit - current_count - cost)
            reset_time = int(now + self.period)

            headers = {
                "X-RateLimit-Limit": str(self.requests_limit),
                "X-RateLimit-Remaining": str(remaining),
                "X-RateLimit-Reset": str(reset_time),
            }

            if not is_allowed:
                headers["Retry-After"] = str(self.period)
                logger.warning(f"Rate limit exceeded for key: {key}")

            return is_allowed, headers

        except Exception as e:
            logger.error(f"Rate limiter error: {e}")
            return True, {
                "X-RateLimit-Limit": str(self.requests_limit),
                "X-RateLimit-Remaining": "0",
                "X-RateLimit-Reset": str(int(now + self.period)),
            }

    async def get_usage(self, key: str) -> dict:
        now = time.time()
        window_start = now - self.period
        redis_key = f"rate_limit:{key}"

        try:
            await redis_client._redis.zremrangebyscore(redis_key, 0, window_start)
            count = await redis_client._redis.zcard(redis_key)

            return {
                "limit": self.requests_limit,
                "remaining": max(0, self.requests_limit - count),
                "reset": int(now + self.period),
                "used": count,
            }
        except Exception as e:
            logger.error(f"Rate limiter get_usage error: {e}")
            return {
                "limit": self.requests_limit,
                "remaining": 0,
                "reset": int(now + self.period),
                "used": 0,
            }


rate_limiter = RateLimiter()

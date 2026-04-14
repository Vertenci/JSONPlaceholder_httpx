import logging
from typing import Any
from .http_client import HTTPClient

logger = logging.getLogger(__name__)


class JSONPlaceholderClient:
    def __init__(self, http_client: HTTPClient):
        self.http_client = http_client

    async def get_all_posts(self, limit: int | None = None) -> list[dict[str, Any]]:
        logger.info("Fetching all posts from JSONPlaceholder")
        posts = await self.http_client.get("/posts")

        if limit:
            posts = posts[:limit]

        return posts

    async def get_post_by_id(self, post_id: int) -> dict[str, Any] | None:
        logger.info(f"Fetching post {post_id} from JSONPlaceholder")
        try:
            return await self.http_client.get(f"/posts/{post_id}")
        except Exception as e:
            logger.error(f"Post {post_id} not found: {e}")
            return None

    async def get_posts_by_user(self, user_id: int) -> list[dict[str, Any]]:
        logger.info(f"Fetching posts for user {user_id}")
        return await self.http_client.get("/posts", params={"userId": user_id})

    async def create_post(self, user_id: int, title: str, body: str) -> dict[str, Any]:
        logger.info(f"Creating post for user {user_id}")
        return await self.http_client.post("/posts", json={
            "userId": user_id,
            "title": title,
            "body": body
        })

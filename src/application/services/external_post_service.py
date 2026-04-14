import logging
from src.infrastructure.external_apis.jsonplaceholder_client import JSONPlaceholderClient
from src.application.dtos.post_dto import PostResponseDTO

logger = logging.getLogger(__name__)


class ExternalPostService:
    def __init__(self, jsonplaceholder_client: JSONPlaceholderClient):
        self._api_client = jsonplaceholder_client

    async def get_all_posts(self, limit: int | None = None) -> list[PostResponseDTO]:
        logger.info(f"Getting all posts (limit={limit})")

        posts_data = await self._api_client.get_all_posts(limit)

        return [
            PostResponseDTO(
                id=post["id"],
                user_id=post["userId"],
                title=post["title"],
                body=post["body"]
            )
            for post in posts_data
        ]

    async def get_post(self, post_id: int) -> PostResponseDTO | None:
        logger.info(f"Getting post {post_id}")

        post_data = await self._api_client.get_post_by_id(post_id)

        if not post_data:
            return None

        return PostResponseDTO(
            id=post_data["id"],
            user_id=post_data["userId"],
            title=post_data["title"],
            body=post_data["body"]
        )

    async def get_user_posts(self, user_id: int) -> list[PostResponseDTO]:
        logger.info(f"Getting posts for user {user_id}")

        posts_data = await self._api_client.get_posts_by_user(user_id)

        return [
            PostResponseDTO(
                id=post["id"],
                user_id=post["userId"],
                title=post["title"],
                body=post["body"]
            )
            for post in posts_data
        ]

    async def create_external_post(self, user_id: int, title: str, body: str) -> PostResponseDTO:
        logger.info(f"Creating external post for user {user_id}")

        post_data = await self._api_client.create_post(user_id, title, body)

        return PostResponseDTO(
            id=post_data["id"],
            user_id=post_data["userId"],
            title=post_data["title"],
            body=post_data["body"]
        )

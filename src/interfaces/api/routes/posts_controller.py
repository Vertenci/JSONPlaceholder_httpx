from fastapi import APIRouter, Depends, HTTPException, status, Query
from src.application.services.external_post_service import ExternalPostService
from src.interfaces.api.schemas.post_schema import CreatePostRequest, PostResponse
from src.interfaces.api.dependencies import get_external_post_service
import logging


logger = logging.getLogger(__name__)


router = APIRouter(prefix="/external/posts", tags=["External Posts"])


@router.get("/")
async def get_all_posts(
    limit: int | None = Query(None, ge=1, le=100),
    service: ExternalPostService = Depends(get_external_post_service)
):
    posts = await service.get_all_posts(limit)
    return [PostResponse.model_validate(post) for post in posts]


@router.get("/{post_id}")
async def get_post(
    post_id: int,
    service: ExternalPostService = Depends(get_external_post_service)
):
    post = await service.get_post(post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {post_id} not found"
        )
    return PostResponse.model_validate(post)


@router.get("/user/{user_id}")
async def get_user_posts(
    user_id: int,
    service: ExternalPostService = Depends(get_external_post_service)
):
    posts = await service.get_user_posts(user_id)
    return [PostResponse.model_validate(post) for post in posts]


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_post(
    data: CreatePostRequest,
    service: ExternalPostService = Depends(get_external_post_service)
):
    try:
        post = await service.create_external_post(
            data.user_id,
            data.title,
            data.body
        )
        return PostResponse.model_validate(post)
    except Exception as e:
        logger.error(f"Failed to create post: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create post in external API"
        )

import logging

from fastapi import APIRouter, Depends, HTTPException, Query
from starlette import status
from src.application.dtos.user_dto import CreateUserDTO, UpdateUserDTO
from src.application.services.user_service import UserService
from src.interfaces.api.dependencies.services import get_user_service
from src.interfaces.api.schemas.user_schema import UserResponse, CreateUserRequest, UpdateUserRequest

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
        data: CreateUserRequest,
        service: UserService = Depends(get_user_service),
):
    try:
        create_dto = CreateUserDTO(
            email=data.email,
            username=data.username,
            full_name=data.full_name,
        )
        user = await service.create_user(create_dto)
        return UserResponse.model_validate(user)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Unexpected error in create_user: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/", response_model=list[UserResponse])
async def get_all_users(
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=1000),
        service: UserService = Depends(get_user_service),
):
    users = await service.get_all_users(skip, limit)
    return [UserResponse.model_validate(user) for user in users]


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    service: UserService = Depends(get_user_service)
):
    user = await service.get_user(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    return UserResponse.model_validate(user)


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    data: UpdateUserRequest,
    service: UserService = Depends(get_user_service)
):
    update_dto = UpdateUserDTO(
        email=data.email,
        username=data.username,
        full_name=data.full_name,
        is_active=data.is_active
    )
    user = await service.update_user(user_id, update_dto)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    return UserResponse.model_validate(user)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    service: UserService = Depends(get_user_service)
):
    deleted = await service.delete_user(user_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )

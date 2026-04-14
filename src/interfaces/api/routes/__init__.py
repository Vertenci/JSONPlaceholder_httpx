from .user_controller import router as user_router
from .profile_controller import router as profile_router
from .posts_controller import router as posts_router
from .weather_controller import router as weather_router

__all__ = ["user_router", "profile_router", "posts_router", "weather_router"]

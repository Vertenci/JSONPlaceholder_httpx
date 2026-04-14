from contextlib import asynccontextmanager
from fastapi import FastAPI
import logging
from starlette.middleware.cors import CORSMiddleware
from src.infrastructure.config.settings import settings
from src.infrastructure.di.container import get_container
from src.interfaces.api.routes import (
    user_controller,
    profile_controller,
    posts_controller,
    weather_controller
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up...")
    container = get_container()
    await container.initialize()
    yield
    logger.info("Shutting down...")
    await container.close()


app = FastAPI(
    title=settings.APP_NAME,
    description="Integration with JSONPlaceholder and OpenWeatherMap APIs",
    version="1.0.0",
    lifespan=lifespan,
    debug=settings.APP_DEBUG,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_controller.router)
app.include_router(profile_controller.router)
app.include_router(posts_controller.router)
app.include_router(weather_controller.router)

@app.get("/health")
async def health():
    return {"status": "healthy", "service": settings.APP_NAME}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.APP_DEBUG,
    )

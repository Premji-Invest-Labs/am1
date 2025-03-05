from fastapi import FastAPI

from app.api.v1.endpoints import health, task
from app.core.logging import get_logger, logger_file_name
from app.core.settings import settings

# Get logger
logger = get_logger(logger_file_name)
logger.debug(f"Current env: {settings.ENV}")

# FastAPI app instance
app = FastAPI(
    title=settings.APP_NAME,
    description="AM1 API for doing general complex tasks using computer with a small team of GenAI Agents.",
    version="0.0.1",
)

# Include API routers
app.include_router(task.router, prefix="/api/v1", tags=["Task"])
app.include_router(health.router, prefix="/api/v1", tags=["Health"])


@app.get("/")
def home():
    logger.info("AM1 Backend is up & running!")
    return {"message": "AM1 Backend is up & running!"}

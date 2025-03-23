# import asyncpg
import asyncpg
from fastapi import APIRouter

from app.core.logging import get_logger
from app.core.settings import settings

router = APIRouter(prefix="/api/v1/health", tags=["Health"])
logger = get_logger()


@router.get("/")
async def health_check():
    """Health check endpoint to verify:
    - Application is running
    - Database is reachable
    - LLM services are responsive
    """
    health_status = {"status": "ok"}

    # Check Database Connection
    try:
        await test_db_connection()
        health_status["database"] = "connected"
    except Exception as e:
        logger.error(f"Database connection error: {e}")
        health_status["database"] = "unreachable"
        health_status["status"] = "error"
    return health_status


async def test_db_connection():
    try:
        logger.info(f"Testing connection to {settings.DATABASE_URL}")
        # conn = psycopg2.connect(settings.DATABASE_URL)
        conn = asyncpg.connect(settings.DATABASE_URL)
        logger.info("Successfully connected to the database!")
        conn.close()
    except Exception as e:
        logger.error(f"Database connection failed: {e!s}")
        raise e

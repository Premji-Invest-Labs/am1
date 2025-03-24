import asyncio
import logging
import os

from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware

from app.api.v1.endpoints import health, task
from app.core.logging import get_logger
from app.core.settings import settings
from app.db.database import sessionmanager
from app.services.kafka.consumer import KafkaConsumer
from app.services.kafka.producer import KafkaProducer

# from app.db.database import get_db

# Get Kafka connection details from environment variables
# KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
# KAFKA_TOPIC = "background_jobs"

# # Create Kafka producer and consumer
# producer = KafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)
# consumer = KafkaConsumer(
#     bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
#     topic=KAFKA_TOPIC,
#     group_id="background_processor"
# )

# Get logger
logger = get_logger()
logger.debug(f"Current env: {settings.ENV}")

# FastAPI app instance
app = FastAPI(
    title=settings.APP_NAME,
    description="AM1 API for doing general complex tasks using computer with a small team of GenAI Agents.",
    version="0.0.1",
)


@app.on_event("startup")
async def startup_event():
    sessionmanager.init()
    print("Database initialized")
    async with sessionmanager.connect() as connection:
        logger.info(f"Tables being created for {settings.DATABASE_URL}")
        print(f"Tables being created for {settings.DATABASE_URL}")
        await sessionmanager.create_all(connection)
    # await producer.start()
    # await consumer.start()
    ## Start consuming messages in a background task
    # asyncio.create_task(consumer.consume())
    print("Database and tables created")


@app.on_event("shutdown")
async def shutdown():
    await sessionmanager.close()
    # await producer.stop()
    # await consumer.stop()


# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("uvicorn.error")


# Middleware to log request details
class LogInvalidRequestsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        try:
            response = await call_next(request)
            return response
        except Exception as e:
            logger.error(f"Invalid Request: {request.method} {request.url} - {e}")
            raise e


# Add middleware to FastAPI
app.add_middleware(LogInvalidRequestsMiddleware)

# Enable CORS to allow requests from any domain
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Specify allowed frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(task.router)
app.include_router(health.router)


@app.get("/")
def home():
    logger.info("AM1 Backend is up & running!")
    return {"message": "AM1 Backend is up & running!"}

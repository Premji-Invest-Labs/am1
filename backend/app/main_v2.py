import logging

import uvicorn
from fastapi import FastAPI

from app.api import router as tasks_router
from app.config import settings
from app.database import Database

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Task API", description="Task management API with PostgreSQL")

# Add routes
app.include_router(tasks_router)

# Database connection events
@app.on_event("startup")
async def startup():
    """Connect to the database on startup"""
    db = Database(settings.DATABASE_URL)
    await db.connect()
    app.state.db = db
    logger.info("Application startup: Connected to database")

@app.on_event("shutdown")
async def shutdown():
    """Disconnect from the database on shutdown"""
    await app.state.db.disconnect()
    logger.info("Application shutdown: Disconnected from database")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
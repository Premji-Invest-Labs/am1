from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.logging import get_logger, logger_file_name
from app.core.settings import settings

# Logger initialization
logger = get_logger(logger_file_name)

# Ensure DATABASE_URL is using `psycopg2` for synchronous operations
if not settings.DATABASE_URL.startswith("postgresql"):
    raise ValueError("Invalid database URL: Must use 'postgresql://'")

# Create synchronous engine with the correct driver (psycopg2)
sync_engine = create_engine(settings.DATABASE_URL, echo=True)

# Create sessionmaker bound to the sync engine
session_factory = sessionmaker(sync_engine, expire_on_commit=False)


# Dependency to get the DB session
def get_relational_db():
    session = session_factory()
    logger.info(f"Resolved session type: {type(session).__name__}")
    return session

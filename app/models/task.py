from uuid import uuid4

from sqlalchemy import Boolean, Column, DateTime, String, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.ext.declarative import declarative_base

# Base class for SQLAlchemy models
Base = declarative_base()


class Task(Base):
    __tablename__ = "tasks"
    task_id = Column(UUID, primary_key=True, index=True, default=uuid4, nullable=False)
    query = Column(String)
    multi_agent_framework = Column(String)
    llm_model = Column(String)
    enable_internet = Column(Boolean)
    status = Column(String)
    task_metadata = Column(JSONB)
    final_response = Column(String)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )

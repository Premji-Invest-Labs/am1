import os
from datetime import datetime as dt
from typing import ClassVar

import yaml
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Load environment variables from .env
load_dotenv()
env = os.getenv("ENV", "local")

# Define the config file path
CONFIG_FILE: str = f"config/{env}.yml"

now_str: str = dt.now().strftime("%Y%m%d-%H%M%S")

# Load YAML file BEFORE defining the Pydantic class
config_data = {}
if os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE) as f:
        config_data = yaml.safe_load(f) or {}


class Settings(BaseSettings):
    # Class variable to avoid Pydantic treating it as a field
    CONFIG_FILE: ClassVar[str] = CONFIG_FILE

    # Define settings using YAML or environment variables
    APP_NAME: str = config_data.get("app", {}).get("name", "FastAPI Default")
    DEBUG: bool = os.getenv(
        "DEBUG", str(config_data.get("app", {}).get("debug", False))
    ).lower() in ("true", "1")

    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        config_data.get("database", {}).get(
            "url", "postgresql://postgres:user@am1_postgres_db:5432/am1"
        ),
    )
    # DATABASE_URL: str = (
    #     "postgresql://postgres:user@localhost:5432/am1"  # Local outside docker
    # )

    OPENAI_API_KEY: str = os.getenv(
        "OPENAI_API_KEY",
        config_data.get("llm_providers", {}).get("openai", {}).get("api_key", "no-key"),
    )

    LOGS_DIR: str = os.getenv(
        "LOGS_DIR", config_data.get("logs", {}).get("logs_dir", "logs")
    )
    LOG_FILE: str = os.getenv(
        "LOG_FILE",
        config_data.get("logs", {}).get(
            "log_file", f"logs/{APP_NAME.replace(':', '')}-{now_str}.log"
        ),
    )

    ENV: str = env


# Instantiate settings
settings = Settings()

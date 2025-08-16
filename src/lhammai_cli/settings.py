"""Configuration for the application."""

from dotenv import find_dotenv, load_dotenv
from pydantic import AnyHttpUrl, Field
from pydantic_settings import BaseSettings

load_dotenv(find_dotenv(".default.env", usecwd=True))
load_dotenv(find_dotenv(".env", usecwd=True), override=True)


class Settings(BaseSettings):
    """Set application settings."""
    api_base: AnyHttpUrl = Field(validation_alias="API_BASE")

    # logging
    log_level: str = Field(validation_alias="LOG_LEVEL", default="DEBUG")
    log_file: str = Field(validation_alias="LOG_FILE", default="app.log")
    log_retention: str = Field(validation_alias="LOG_RETENTION", default="10 days")


settings = Settings()  # type: ignore

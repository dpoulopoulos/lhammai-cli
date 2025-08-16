"""Configuration for the application."""

from dotenv import find_dotenv, load_dotenv
from pydantic import AnyHttpUrl, Field
from pydantic_settings import BaseSettings

load_dotenv(find_dotenv(".default.env", usecwd=True))
load_dotenv(find_dotenv(".env", usecwd=True), override=True)


class Settings(BaseSettings):
    """Set application settings."""
    api_base: AnyHttpUrl = Field(validation_alias="API_BASE")


settings = Settings()  # type: ignore

from any_llm.exceptions import UnsupportedProviderError
from any_llm.provider import ProviderFactory
from dotenv import find_dotenv, load_dotenv
from pydantic import AnyHttpUrl, Field, ValidationError, field_validator
from pydantic_settings import BaseSettings

load_dotenv(find_dotenv(".default.env", usecwd=True))
load_dotenv(find_dotenv(".env", usecwd=True), override=True)


class Settings(BaseSettings):
    """Set application settings."""
    # LLM settings
    model: str = Field(validation_alias="MODEL")
    api_base: AnyHttpUrl = Field(validation_alias="API_BASE")

    # logging
    log_level: str = Field(validation_alias="LOG_LEVEL", default="DEBUG")
    log_file: str = Field(validation_alias="LOG_FILE", default="app.log")
    log_retention: str = Field(validation_alias="LOG_RETENTION", default="10 days")

    @field_validator("model")
    @classmethod
    def validate_model(cls, v: str) -> str:
        """Validate that the model follows the expected format.

        Check that the model string is in the format '<provider>/<model>'
        and that the provider is in the `SUPPORTED_PROVIDERS` list.
        """
        try:
            _, _ = ProviderFactory.split_model_provider(v)
        except UnsupportedProviderError:
            raise
        except ValidationError:
            raise

        return v


settings = Settings()  # type: ignore

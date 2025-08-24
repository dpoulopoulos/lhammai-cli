import pytest
from any_llm.exceptions import UnsupportedProviderError
from pydantic import ValidationError

from lhammai_cli.settings import Settings


def test_settings_valid_model(monkeypatch):
    """Test that a valid model is accepted."""
    model = "ollama:test-model:latest"
    monkeypatch.setenv("MODEL", model)
    monkeypatch.setenv("API_BASE", "http://localhost:11434")
    settings = Settings()  # type: ignore
    assert settings.model == model


def test_settings_invalid_model_format(monkeypatch):
    """Test that a validation error is raised for an invalid model format."""
    monkeypatch.setenv("MODEL", "invalid-model-format")
    monkeypatch.setenv("API_BASE", "http://localhost:11434")
    with pytest.raises(ValidationError) as excinfo:
        Settings()  # type: ignore
    assert "Value error, Invalid model format." in str(excinfo.value)


def test_settings_unsupported_provider(monkeypatch):
    """Test that a validation error is raised for an unsupported provider."""
    monkeypatch.setenv("MODEL", "unsupported:model:latest")
    monkeypatch.setenv("API_BASE", "http://localhost:11434")
    with pytest.raises(UnsupportedProviderError) as excinfo:
        Settings()  # type: ignore
    assert "'unsupported' is not a supported provider." in str(excinfo.value)


def test_settings_unsupported_api_base(monkeypatch):
    """Test that a validation error is raised for an unsupported API base."""
    monkeypatch.setenv("MODEL", "ollama:test-model:latest")
    monkeypatch.setenv("API_BASE", "ftp://localhost:11434")
    with pytest.raises(ValidationError) as excinfo:
        Settings()  # type: ignore
    error_message = ("URL scheme should be 'http' or 'https' "
                     "[type=url_scheme, input_value='ftp://localhost:11434', input_type=str]")
    assert error_message in str(excinfo.value)

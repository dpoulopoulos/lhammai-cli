from unittest.mock import MagicMock, patch

import pytest
from any_llm.types.completion import ChatCompletion
from ollama._types import ResponseError

from lhammai_cli.utils.llm_utils import get_llm_response


def test_get_llm_response_success(mock_llm_response: ChatCompletion) -> None:
    """Test successful response from the LLM."""
    with patch("lhammai_cli.utils.llm_utils.completion") as mock_completion:
        mock_completion.return_value = mock_llm_response

        model = "ollama/test_model"
        api_base = "http://localhost:11434"
        prompt = "Hello!"

        response = get_llm_response(prompt, model, api_base)  # type: ignore

        assert response == "This is a mock response!"
        mock_completion.assert_called_once_with(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            api_base=api_base
        )


def test_get_llm_response_connection_error() -> None:
    """Test connection error when communicating with the LLM."""
    with patch("lhammai_cli.utils.llm_utils.completion", side_effect=ConnectionError("Test error")) as mock_completion:
        model = "ollama/test_model"
        api_base = "http://localhost:11434"
        prompt = "Hello!"

        with pytest.raises(ConnectionError):
            get_llm_response(prompt, model, api_base)  # type: ignore

        mock_completion.assert_called_once_with(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            api_base=api_base
        )


def test_get_llm_response_streaming_not_implemented() -> None:
    """Test model not found error."""
    with patch(
        "lhammai_cli.utils.llm_utils.completion",
        side_effect=ResponseError("model \"test_model\" not found, try pulling it first (status code: 404)")
    ) as mock_completion:
        model = "ollama/test_model"
        api_base = "http://localhost:11434"
        prompt = "Hello!"

        with pytest.raises(ResponseError):
            get_llm_response(prompt, model, api_base)  # type: ignore

    mock_completion.assert_called_once_with(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        api_base=api_base
    )


def test_get_llm_response_invalid_response() -> None:
    """Test invalid response from the LLM."""
    with patch("lhammai_cli.utils.llm_utils.completion") as mock_completion:
        mock_completion.return_value = MagicMock()

        model = "ollama/test_model"
        api_base = "http://localhost:11434"
        prompt = "Hello!"

        with pytest.raises(RuntimeError):
            get_llm_response(prompt, model, api_base)  # type: ignore

    mock_completion.assert_called_once_with(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        api_base=api_base
    )

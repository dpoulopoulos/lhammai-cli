"""Unit tests for LLM utility functions."""

from unittest.mock import MagicMock, patch

import pytest
from any_llm.types.completion import ChatCompletion
from pytest_mock import MockerFixture

from lhammai_cli.utils.llm_utils import get_llm_response


def test_get_llm_response_success(mock_llm_response: ChatCompletion) -> None:
    """Test successful response from the LLM."""
    with patch("lhammai_cli.utils.llm_utils.completion") as mock_completion:
        mock_completion.return_value = mock_llm_response

        model = "ollama/test_model"
        api_base = "http://localhost:11434"
        messages = [{"role": "user", "content": "Hello!"}]

        response = get_llm_response(messages, model, api_base)  # type: ignore

        assert response == "This is a mock response!"
        mock_completion.assert_called_once_with(
            model=model,
            messages=messages,
            api_base=api_base
        )


def test_get_llm_response_connection_error() -> None:
    """Test connection error when communicating with the LLM."""
    with patch("lhammai_cli.utils.llm_utils.completion", side_effect=ConnectionError("Test error")) as mock_completion:
        model = "ollama/test_model"
        api_base = "http://localhost:11434"
        messages = [{"role": "user", "content": "Hello"}]

        with pytest.raises(ConnectionError):
            get_llm_response(messages, model, api_base)  # type: ignore
        
        mock_completion.assert_called_once_with(
            model=model,
            messages=messages,
            api_base=api_base
        )


def test_get_llm_response_streaming_not_implemented(mocker: MockerFixture) -> None:
    """Test streaming response not implemented error."""
    mock_streaming_response = iter([MagicMock()])
    with patch(
        "lhammai_cli.utils.llm_utils.completion",
        return_value=mock_streaming_response,
    ) as mock_completion:
        model = "ollama/test_model"
        api_base = "http://localhost:11434"
        messages = [{"role": "user", "content": "Hello"}]

        with pytest.raises(NotImplementedError):
            get_llm_response(messages, model, api_base) # type: ignore

    mock_completion.assert_called_once_with(
        model=model,
        messages=messages,
        api_base=api_base
    )

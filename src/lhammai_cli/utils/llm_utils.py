"""Utility functions for interacting with LLMs."""

from collections.abc import Iterator
from typing import Any

from any_llm import completion
from any_llm.types.completion import ChatCompletion, ChatCompletionChunk, ChatCompletionMessage
from halo import Halo
from rich.console import Console

from .logging import logger

console = Console()


def get_llm_response(messages: list[dict[str, Any] | ChatCompletionMessage], model: str, api_base: str) -> str | None:
    """Get a response from the LLM.

    Args:
        messages (list[dict[str, Any]]): The messages to send to the LLM.
        model (str): The LLM model to use.
        api_base (str): The provider's API base URL.

    Returns:
        str: The LLM's response.

    Raises:
        ConnectionError: If the connection to the LLM fails.
        NotImplementedError: For streaming responses.
    """
    provider, _ = model.split('/')

    spinner = Halo(
        text='🤖 Thinking...',
        spinner='dots',
        color='cyan'
    )

    logger.debug(f"Sending prompt to model {model} at {api_base}...")

    spinner.start()
    try:
        response:  ChatCompletion | Iterator[ChatCompletionChunk] = completion(
            model=model,
            messages=messages,
            api_base=api_base
        )
    except ConnectionError as e:
        spinner.stop()
        logger.error(f"Failed to connect to {provider.capitalize()} - {e}")
        raise
    except Exception as e:
        spinner.stop()
        logger.error(f"An error occurred while communicating with {provider.capitalize()}: {e}")
        raise

    if isinstance(response, ChatCompletion):
        spinner.stop()
        return response.choices[0].message.content
    else:
        spinner.stop()
        logger.error("Streaming responses are not supported yet.")
        raise NotImplementedError(
            "Streaming responses are not supported yet."
        )

"""Utility functions for interacting with LLMs."""

from collections.abc import Iterator

from any_llm import completion
from any_llm.types.completion import ChatCompletion, ChatCompletionChunk
from halo import Halo


def get_llm_response(prompt: str, model: str, api_base: str) -> str | None:
    """Get a response from the LLM.

    Args:
        prompt (str): The prompt to send to the LLM.
        model (str): The LLM model to use.
        api_base (str): The provider's API base URL.

    Returns:
        str: The LLM's response.
    """
    spinner = Halo(
        text='🤖 Thinking...',
        spinner='dots',
        color='cyan'
    )

    spinner.start()
    response:  ChatCompletion | Iterator[ChatCompletionChunk] = completion(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        api_base=api_base
    )
    spinner.stop()

    if isinstance(response, ChatCompletion):
        return response.choices[0].message.content
    else:
        raise NotImplementedError(
            "Streaming responses are not supported yet."
        )

import pytest
from any_llm.types.completion import ChatCompletion, ChatCompletionMessage, Choice, CompletionUsage


@pytest.fixture(scope="session")
def mock_llm_response() -> ChatCompletion:
    """Mock response for LLM calls."""
    return ChatCompletion(
        id="chatcmpl-34cbfe5f-efd9-490d-a525-a00b35bee495",
        choices=[
            Choice(
                finish_reason="stop",
                index=0,
                message=ChatCompletionMessage(
                    content="This is a mock response!",
                    role="assistant",
                ),
            )
        ],
        created=1677652288,
        model="gemma3:4b",
        object="chat.completion",
        system_fingerprint=None,
        usage=CompletionUsage(
            completion_tokens=7, prompt_tokens=3, total_tokens=10
        ),
    )

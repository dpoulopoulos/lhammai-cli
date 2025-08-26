import tempfile
from pathlib import Path

import pytest
from any_llm.types.completion import ChatCompletion, ChatCompletionMessage, Choice, CompletionUsage

from lhammai_cli.history import ConversationHistory


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
        usage=CompletionUsage(completion_tokens=7, prompt_tokens=3, total_tokens=10),
    )


@pytest.fixture
def sample_conversation() -> list[dict[str, str]]:
    """Sample conversation data for testing."""
    return [
        {"role": "user", "content": "Hello, how are you?"},
        {"role": "assistant", "content": "I'm doing well, thank you! How can I help you today?"},
        {"role": "user", "content": "Can you explain what Python is?"},
        {
            "role": "assistant",
            "content": "Python is a high-level programming language known for its simplicity and readability.",
        },
    ]


@pytest.fixture
def temp_history_file():
    """Create a temporary file for history."""
    with tempfile.NamedTemporaryFile(delete=True, suffix=".json") as f:
        yield Path(f.name)


@pytest.fixture
def conversation_history_with_data(sample_conversation, temp_history_file, monkeypatch):
    """Create a ConversationHistory instance with sample data."""
    from lhammai_cli import history
    
    monkeypatch.setattr(history, "HISTORY_FILE", temp_history_file)
    history_instance = ConversationHistory.start_new(model="ollama:gemma3:4b", api_base="http://localhost:11434")

    for message in sample_conversation:
        from lhammai_cli.schema import Role
        history_instance.add_message(Role(message["role"]), message["content"])

    return history_instance

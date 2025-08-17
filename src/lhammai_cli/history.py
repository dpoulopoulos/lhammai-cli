"""Conversation history management for any-cli."""

from typing import Any, Literal

from any_llm.types.completion import ChatCompletionMessage

from lhammai_cli.schemas import Message, Role


class ConversationHistory:
    """Manages the conversation history for a user."""
    def __init__(self) -> None:
        """Initializes the conversation history."""
        self.messages = []

    def add_message(self, role: Literal[Role.USER, Role.ASSISTANT], content: str) -> None:
        """Adds a message to the conversation history.

        Args:
            role (Role): The role of the message sender (user or assistant).
            content (str): The content of the message.
        """
        message = Message(role=role, content=content)
        self.messages.append(message.model_dump())

    def get_history(self) -> list[dict[str, Any] | ChatCompletionMessage]:
        """Returns the conversation history.

        Returns:
            list[dict[str, Any] | ChatCompletionMessage]: The conversation history.
        """
        return self.messages

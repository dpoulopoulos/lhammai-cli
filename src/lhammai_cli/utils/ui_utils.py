"""Utility functions for drawing rich visual elements."""

from typing import Any

from rich.markdown import Markdown
from rich.panel import Panel

type_mapping = {
    "info": "💡 Info",
    "error": "❌ Error",
    "success": "✅ Success",
    "assistant": "🤖 Assistant",
}


def draw_panel(content: Any, type: str) -> Panel:
    """Draw a panel with the given title and content."""
    border_style = "green"

    if type == "assistant":
        content = Markdown(content)

    if type == "error":
        border_style = "red"

    return Panel(
        content,
        title=type_mapping[type],
        title_align="left",
        border_style=border_style,
        padding=(1, 1)
    )

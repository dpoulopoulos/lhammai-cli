"""The main entrypoint of the application."""

import click
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

from lhammai_cli.settings import settings
from lhammai_cli.utils import draw_panel, get_llm_response

console = Console()


@click.command
@click.argument("prompt", required=True)
@click.option("--model", "-m", default='ollama/gemma3:4b', help='LLM model to use')
@click.option("--api-base", default=settings.api_base, help='Host to connect to')
def main(prompt: str, model: str, api_base: str) -> None:
    """Interact with any LLM from the command line.

    Args:
        prompt (str): The prompt to send to the LLM.
        model (str): The LLM model to use.
        api_base (str): The provider's API base URL.
    """
    info_message = draw_panel(
        content=f"You are chatting with [cyan]'{model}'[/cyan] at [cyan]'{api_base}'[/cyan]...",
        type="info"
    )
    console.print(info_message)

    response = get_llm_response(prompt, model, api_base)
    if response:
        response_panel = draw_panel(
            content=response,
            type="assistant"
        )
        console.print(response_panel)
    else:
        error_panel = draw_panel(
            content=f"Failed to get a response from the model '{model}'.",
            type="error"
        )
        console.print(error_panel)

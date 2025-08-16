"""The main entrypoint of the application."""

import click
from rich.console import Console

from lhammai_cli.settings import settings
from lhammai_cli.utils import get_llm_response

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
    console.print(f"\n✨ Using model: [cyan]{model}[/cyan]")
    response = get_llm_response(prompt, model, api_base)
    if response:
        console.print(f"\n🤖 LLM response: [green]{response}[/green]")
    else:
        console.print(f"\n❌ LLM response: [red]No response received from {model}[/red]")

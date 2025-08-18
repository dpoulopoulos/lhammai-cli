import click
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

from lhammai_cli.settings import settings
from lhammai_cli.utils import get_llm_response

console = Console()


@click.command
@click.argument("prompt", required=True)
@click.option("--model", "-m", default=settings.model, help='LLM model to use')
@click.option("--api-base", default=settings.api_base, help='Host to connect to')
def main(prompt: str, model: str, api_base: str) -> None:
    """Interact with any LLM."""
    console.print(f"\n✨ Connected to [cyan]'{model}'[/cyan] at [cyan]'{api_base}'[/cyan]\n")

    try:
        response = get_llm_response(prompt, model, api_base)
        if response:
            response_panel = Panel(
                Markdown(response),
                title="🤖 Assistant",
                title_align="left",
                border_style="cyan",
                padding=(1, 1)
            )
            console.print(response_panel)
        else:
            console.print(f"\n❌ LLM response: [red]No response received from {model}[/red]")
    except (ConnectionError, RuntimeError, Exception) as e:
        console.print(f"\n❌ An error occurred: [red]{e}[/red]")

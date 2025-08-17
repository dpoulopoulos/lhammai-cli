"""The main entrypoint of the application."""

from importlib.metadata import version as pkg_version

import click
from rich.console import Console

from lhammai_cli.history import ConversationHistory
from lhammai_cli.schemas import Role
from lhammai_cli.settings import settings
from lhammai_cli.utils import draw_panel, get_llm_response

console = Console()


def _get_llm_response(messages: ConversationHistory, model: str, api_base: str) -> str | None:
    """Helper function to get a response from the LLM and handle errors."""
    provider, _ = model.split('/')

    try:
        response = get_llm_response(messages.get_history(), model, api_base)
        if not response:
            return
    except ConnectionError:
        error_panel = draw_panel(
            content=f"Failed to connect to [red]{provider.capitalize()}[/red] at [red]{api_base}[/red]. "
                    "Please check your settings.",
            type="error"
        )
        console.print(error_panel)
        return
    except NotImplementedError:
        error_panel = draw_panel(
            content="Streaming responses are not supported yet.",
            type="error"
        )
        console.print(error_panel)
        return
    except Exception as e:
        error_panel = draw_panel(
            content=f"An unexpected error occurred: {e}",
            type="error"
        )
        console.print(error_panel)
        return

    return response


def show_logo(model: str, api_base: str):
    """Display the Lhammai logo with rich formatting."""
    try:
        version = pkg_version("lhammai-cli")
    except Exception:
        version = "unknown"
    
    logo = f"""
    ╭───────────────────────────────────────────╮
    │           🚀 Lhammai v{version}               │
    │ Interact with any LLM from your terminal. │
    ╰───────────────────────────────────────────╯
    """
    console.print(f"[cyan]{logo}[/cyan]")
    console.print("💡 [cyan]Interactive[/cyan] mode activated. Type [cyan]'/exit'[/cyan] to end the session.")
    console.print("🧹 Type [cyan]'/clear'[/cyan] to clear the screen.")
    console.print(f"✨ You are chatting with [cyan]'{model}'[/cyan] at [cyan]'{api_base}'[/cyan].\n")


@click.command
@click.option("--prompt", "-p", help="The prompt to send to the LLM")
@click.option('--interactive', '-i', is_flag=True, help='Run in interactive mode')
@click.option("--model", "-m", default='ollama/gemma3:4b', help='LLM model to use')
@click.option("--api-base", default=settings.api_base, help='Host to connect to')
def main(prompt: str, interactive: bool, model: str, api_base: str) -> None:
    """Interact with any LLM from the command line.

    Args:
        prompt (str): The prompt to send to the LLM.
        interactive (bool): Whether to run in interactive mode.
        model (str): The LLM model to use.
        api_base (str): The provider's API base URL.
    """
    history = ConversationHistory()
    if interactive:
        show_logo(model, api_base)

        while True:
            user_input = console.input("[bold]🌟 You:[/bold] ")

            if user_input.lower() == '/exit':
                console.print("\n👋 [bold yellow]Thanks for using Lhammai![/bold yellow]")
                break
            elif user_input.lower() == '/clear':
                console.clear()
                show_logo(model, api_base)
                continue

            history.add_message(Role.USER, user_input)
            response = _get_llm_response(history, model, api_base)
            if response:
                history.add_message(Role.ASSISTANT, response)
                response_panel = draw_panel(
                    content=response,
                    type="assistant"
                )
                console.print(response_panel)
    elif prompt:
        history.add_message(Role.USER, prompt)
        response = _get_llm_response(history, model, api_base)

        if response:
            response_panel = draw_panel(
                content=response,
                type="assistant"
            )
            console.print(response_panel)
    else:
        error_panel = draw_panel(
            content="Please provide a prompt or run in interactive mode. Run `lhammai --help` for more information.",
            type="error"
        )
        console.print(error_panel)
        return

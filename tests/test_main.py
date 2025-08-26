from unittest.mock import patch

from click.testing import CliRunner

from lhammai_cli import history
from lhammai_cli.main import main


def test_main_with_prompt_option(temp_history_file, monkeypatch):
    """Test main function with prompt option."""
    monkeypatch.setattr(history, "HISTORY_FILE", temp_history_file)

    runner = CliRunner()
    prompt = "Hello world!"
    return_value = "Hello there!"

    with patch("lhammai_cli.main.get_llm_response", return_value=return_value) as mock_get:
        result = runner.invoke(main, ["-p", prompt], input="")

    assert result.exit_code == 0
    assert return_value in result.output
    mock_get.assert_called_once_with(prompt, "ollama:gemma3:4b", "http://localhost:11434/")

    temp_history_file.unlink()


def test_main_with_stdin_input(temp_history_file, monkeypatch):
    """Test main function with stdin input."""
    monkeypatch.setattr(history, "HISTORY_FILE", temp_history_file)

    runner = CliRunner()
    stdin_content = "Test content from stdin."
    return_value = "Test response."

    with patch("lhammai_cli.main.get_llm_response", return_value=return_value) as mock_get:
        result = runner.invoke(main, input=stdin_content)

    assert result.exit_code == 0
    assert return_value in result.output
    mock_get.assert_called_once_with(stdin_content, "ollama:gemma3:4b", "http://localhost:11434/")

    temp_history_file.unlink()


def test_main_with_stdin_and_prompt(temp_history_file, monkeypatch):
    """Test main function with both stdin and prompt option."""
    monkeypatch.setattr(history, "HISTORY_FILE", temp_history_file)

    runner = CliRunner()
    stdin_content = "This is test content."
    prompt = "summarize:"
    return_value = "Test response."

    with patch("lhammai_cli.main.get_llm_response", return_value=return_value) as mock_get:
        result = runner.invoke(main, ["-p", prompt], input=stdin_content)

    assert result.exit_code == 0
    assert return_value in result.output
    mock_get.assert_called_once_with(f"{prompt} {stdin_content}", "ollama:gemma3:4b", "http://localhost:11434/")

    temp_history_file.unlink()


def test_main_no_input_provided():
    """Test main function with no input provided."""
    runner = CliRunner()
    result = runner.invoke(main)

    assert result.exit_code == 1
    assert "No input provided" in result.output


def test_main_connection_error():
    """Test main function handling connection error."""
    runner = CliRunner()

    with patch("lhammai_cli.main.get_llm_response", side_effect=ConnectionError("Connection failed")):
        result = runner.invoke(main, ["-p", "Hello"])

    assert result.exit_code == 0
    assert "Connection failed" in result.output


def test_main_no_response_received(mock_llm_response):
    """Test main function when no response is received."""
    runner = CliRunner()

    with patch("lhammai_cli.main.get_llm_response", return_value=None):
        result = runner.invoke(main, ["-p", "Hello"])

    assert result.exit_code == 0
    assert "No response received" in result.output

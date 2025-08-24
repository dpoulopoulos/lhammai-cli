test:
	uv run pytest

test-coverage:
	uv run coverage run -m pytest && \
	uv run coverage report -m

install-ollama:
	uv sync --dev --extra ollama

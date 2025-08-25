test:
	uv run pytest

test-coverage:
	uv run coverage run -m pytest && \
	uv run coverage report -m

lint:
	uv run ruff check .

format:
	uv run ruff format .

install-ollama:
	uv sync --dev --extra ollama

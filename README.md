<div align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/images/lhammai-cli-white.svg">
    <img alt="Lhammai CLI logo" src="assets/images/lhammai-cli-black.svg" width="50%">
  </picture>
</div>

<br>

<div align="center">

[![License](https://img.shields.io/badge/license-apache%202.0-blue)](#license)
[![Tests](https://github.com/dpoulopoulos/lhammai-cli/actions/workflows/test.yml/badge.svg)](https://github.com/dpoulopoulos/lhammai-cli/actions/workflows/test.yml)

</div>

<h3 align="center">✨ Interact with any LLM from your terminal</h3>

---

Lhammai CLI allows you to interact with any LLM directly from your terminal using a simple, intuitive interface.
Powered by the [`any-llm`](https://mozilla-ai.github.io/any-llm/) library, it seamlessly connects to various LLM
providers, including OpenAI, Anthropic, and local servers such as Ollama, llamafile, and others. For a full list of
supported providers, see the official [any-llm documentation](https://mozilla-ai.github.io/any-llm/providers/).

## Getting Started

### Prerequisites

- [Python 3.13+](https://www.python.org/downloads/)
- [uv](https://github.com/astral-sh/uv)

### Installation

1. Clone the repository and navigate to the source directory:
   ```bash
   git clone https://github.com/dpoulopoulos/lhammai-cli.git && cd lhammai-cli
   ```

2. Install the dependencies using `uv`:
   ```bash
   uv sync --group ollama
   ```

3. Activate the virtual environment:

   ```bash
   source .venv/bin/activate
   ```

> [!NOTE]
> This installs the necessary dependencies to communicate with a local model via Ollama.

### Usage

To begin, you'll need to run the Ollama server. For this example, you can use Docker for a quick setup.


> [!WARNING]
> This approach has some limitations, especially on a Mac. Since Docker Desktop doesn't support GPUs, it's better to run
> Ollama as a standalone application if you're using a Mac. For more detailed instructions, check the official
> [Ollama documentation](https://github.com/ollama/ollama/tree/main/docs).

1. Run the following command to start the Ollama server in a Docker container:

    a. CPU only:
    ```bash
    docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
    ```

    b. Nvidia GPU:
    ```bash
    docker run -d --gpus=all -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
    ```

2. Run a model:

    ```bash
    docker exec -it ollama ollama run gemma3:4b
    ```

3. Interact with the model:

    ```bash
    lhammai Hello!
    ```

> [!TIP]
> Configure your application by creating a `.env` file in the root directory and adding your options:
> `cp .default.env .env`

# License

See the [LICENSE](LICENSE) file for details.

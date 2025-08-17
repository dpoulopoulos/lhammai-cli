# Lhammai CLI

Lhammai CLI allows you to interact with any LLM directly from your terminal using a simple, intuitive interface.
Powered by the [`any-llm`](https://mozilla-ai.github.io/any-llm/) library, it seamlessly connects to various LLM
providers, including OpenAI, Anthropic, and more. It also supports local models such as Ollama, llamafile, and others.
For a full list of supported providers, see the official
[any-llm documentation](https://mozilla-ai.github.io/any-llm/providers/).

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

   > [!NOTE]
   > This installs the necessary dependencies to communicate with a local model via Ollama.

### Single Turn Mode

In single turn mode, the CLI processes one user input at a time and returns a response. This is useful for quick
questions and answers:

```bash
uv run lhammai -p "Your question here"
```

### Multi Turn Conversations

In multi turn conversations, the CLI maintains context across multiple user inputs. This allows for more natural and
fluid interactions:

```bash
uv run lhammai -i
```

# License

See the [LICENSE](LICENSE) file for details.

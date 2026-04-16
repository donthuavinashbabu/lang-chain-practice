LangChain practice project managed with [uv](https://docs.astral.sh/uv/).

## How this project was set up

The steps below are the commands used to create the environment and dependencies, with a short explanation for each.

### 1. Install uv (Windows PowerShell)

```powershell
powershell -ExecutionPolicy Bypass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Explanation:** Downloads and runs Astral’s official installer script. `irm` (`Invoke-RestMethod`) fetches the script; `iex` (`Invoke-Expression`) runs it. `-ExecutionPolicy Bypass` allows the one-liner to run even when script execution is restricted. This installs the `uv` binary (fast Python package and project manager).

### 2. Add uv to your PATH

**Explanation:** The installer prints the directory where `uv.exe` was placed (commonly `%USERPROFILE%\.local\bin` on Windows). Add that folder to your user **PATH** in **Settings → System → About → Advanced system settings → Environment variables** (or the equivalent in your Windows version) so `uv` works from any terminal without a full path.

### 3. Confirm uv is installed

```bash
uv help
```

**Explanation:** Shows uv’s CLI help and proves the executable is on your PATH.

```bash
uv self version
```

**Explanation:** Prints the installed uv version (and related toolchain info), useful for debugging and documentation.

### 4. Initialize the project

```bash
uv init
```

**Explanation:** Creates a Python project in the current directory: `pyproject.toml`, starter layout, and (with default options) a `.gitignore` suited to Python so virtualenvs, caches, and common junk are not committed.

### 5. Add runtime and dev dependencies

```bash
uv add langchain
```

**Explanation:** Adds the core LangChain library and records it in `pyproject.toml` (and the lockfile if you use one).

```bash
uv add langchain-openai
```

**Explanation:** Adds LangChain integrations for OpenAI models and APIs.

```bash
uv add python-dotenv
```

**Explanation:** Adds `python-dotenv` so `load_dotenv()` can read variables from a `.env` file.

```bash
uv add black isort
```

**Explanation:** Adds **Black** (code formatter) and **isort** (import sorter) as project dependencies for consistent style.

### 6. Python `.gitignore`

**Explanation:** A Python-oriented `.gitignore` (for example the one created by `uv init`, or a standard template) keeps `.venv/`, `__pycache__/`, `.env`, build artifacts, and similar files out of Git. If your repo did not get one, add `.gitignore` before committing.

### 7. More LangChain providers

```bash
uv add langchain-google-genai
```

**Explanation:** Adds LangChain support for Google Generative AI (Gemini, etc.).

```bash
uv add langchain-ollama
```

**Explanation:** Adds LangChain support for [Ollama](https://ollama.com/) so you can run local models.

---

## Running the project

From this directory, sync the environment and run your app as needed, for example:

```bash
uv sync
uv run python main.py
```

Ensure a `.env` file exists locally for secrets (for example API keys); do not commit it.

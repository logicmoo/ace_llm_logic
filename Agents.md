
# Agent Instructions: ace_llm_logic Setup

This project has recently been updated to:

- Use the latest `openai` SDK (`client.chat.completions.create(...)`)
- Automatically start the APE parser in HTTP mode on a random port
- Support optional connection to a pre-running APE server via `--use-http-ape`
- Bundle the APE executable (`ape.exe`) locally — no need to compile
- Include a full CLI interface in `python/ace_llm_logic/__main__.py`

---

## 🔧 Installation Prerequisites (for agent/automation setup)

Before attempting to run the logic pipeline, ensure the following setup steps are run on the system:

```bash
apt update -y
apt install -y swi-prolog-full
pip install -r requirements.txt
pip install -e .
```

These steps:

- Install system-wide SWI-Prolog (required for APE execution)
- Install Python dependencies (OpenAI client, requests, etc.)
- Register the project as an editable Python package for CLI use

---

## 🧠 Default Agent Behavior

By default, the system will:

- Rewrite any natural sentence into ACE-friendly Controlled English
- Start an embedded APE server on a random free port
- Parse the logic and then refine it with GPT-4o
- Shut down the temporary APE server after processing
- Update this for with new behavours

Mock and external APE server modes are available via CLI flags.

---

## 🧪 To Run

```bash
python -m python.ace_llm_logic --file input.txt
```

Use `--mock` for offline use, or `--use-http-ape server:port` to connect to a running server.

---

## 🔄 Last Updated

Auto-generated with latest Python logic and packaging structure. This file should be referenced by agents or shell scripts performing bootstrap or CI setup.

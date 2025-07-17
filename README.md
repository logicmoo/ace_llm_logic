
# ace_llm_logic

A command-line pipeline that converts natural English into first-order logic (FOL) using:

- ✅ LLM (OpenAI GPT-4o) to rewrite to ACE-compatible Controlled English
- ✅ APE parser with ERG grammar to derive formal logical representations
- ✅ LLM again to reintroduce tense, aspect, and passive voice
- ✅ Optional mock mode for development and testing without ACE
- ✅ Automatic APE HTTP server startup with `--use-http-ape` override

---

## 📁 Project Structure

```
ace_llm_logic/
├── python/ace_llm_logic/      # Python source code (CLI & pipeline)
├── APE/                       # Bundled Attempto Parsing Engine
├── tests/                     # Pytest tests
├── requirements.txt
├── pyproject.toml
├── Dockerfile
├── .gitignore
└── README.md
```

---

## 🔧 Requirements

- Python 3.8+
- [OpenAI Python SDK v1.x](https://github.com/openai/openai-python)
- SWI-Prolog (e.g. `apt install -y swi-prolog-full`)
- OpenAI API key
- Bundled APE parser executable

Install dependencies:

```bash
apt update -y
apt install -y swi-prolog-full
pip install -r requirements.txt
pip install -e .
```

---

## 🛠️ APE Parser

This repository ships with the Attempto Parsing Engine under `APE/`.
After installing SWI-Prolog, the CLI automatically launches APE in HTTP mode.
Use `--use-http-ape host:port` to connect to an existing server if desired.

---

## 🚀 Usage

### From a file:

```bash
export OPENAI_API_KEY=sk-...
ace-llm-logic --file input.txt
```

### Interactively:

```bash
ace-llm-logic
```

### Mock Mode (no ACE required):

```bash
ace-llm-logic --mock
```

Connect to an existing APE HTTP server with:

```bash
ace-llm-logic --use-http-ape host:port
```

---

## ✅ Example

Input:
```
The report was written by Alice after she reviewed the data.
```

ACE-friendly rewrite (via GPT):
```
Alice writes the report. Alice reviews the data before that.
```

Final adjusted logic:
```prolog
past(write(alice, report1)).
past(review(alice, data1)).
after(write(alice, report1), review(alice, data1)).
passive_form(write(alice, report1)).
```

---

## 🧪 Testing

```bash
pytest tests/
```

Tests run in `--mock` mode and do not require ACE.

---

## 🐳 Docker

To run inside a container:

```bash
docker build -t ace-llm-logic .
docker run -e OPENAI_API_KEY=sk-... ace-llm-logic
```

---

## 🧠 Why Use This?

This pipeline allows you to:
- Accept natural, unrestricted English
- Normalize it to a controlled syntax (ACE)
- Parse it into precise formal logic
- Recover the original nuance (tense, passive, etc.)

Useful for knowledge extraction, rule-based agents, FOL-based reasoning, or explainable AI.

---

## 📜 License

MIT

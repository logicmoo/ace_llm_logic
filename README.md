
# ace_llm_logic

A command-line pipeline that converts natural English into first-order logic (FOL) using:

- ✅ LLM (OpenAI GPT-4o) to rewrite to ACE-compatible Controlled English
- ✅ ACE parser with ERG grammar to derive formal logical representations
- ✅ LLM again to reintroduce tense, aspect, and passive voice
- ✅ Optional mock mode for development and testing without ACE

---

## 📁 Project Structure

```
ace_llm_logic/
├── python/ace_llm_logic/      # Python source code (CLI & pipeline)
├── ace/bin/                   # Place ACE binary here (e.g. 'ace')
├── ace/grammars/              # Place grammar file here (e.g. 'erg.dat')
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
- OpenAI API key
- Optional: ACE parser & ERG grammar

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 🛠️ Installing ACE (optional, unless using --mock)

```bash
# Clone and build ACE
git clone https://github.com/delph-in/ace.git
cd ace
make

# Place the resulting binary into:
mkdir -p ace/bin/
cp ./ace ace/bin/

# Download ERG grammar:
mkdir -p ace/grammars/
wget http://www.delph-in.net/erg/erg-2020-osx-0.9.30.dat -O ace/grammars/erg.dat
```

You can also use a symlink into `ace/bin/` and drop your grammar in `ace/grammars/`.

---

## 🚀 Usage

### From a file:

```bash
export OPENAI_API_KEY=sk-...
python -m python.ace_llm_logic --file input.txt
```

### Interactively:

```bash
python -m python.ace_llm_logic
```

### Mock Mode (no ACE required):

```bash
python -m python.ace_llm_logic --mock
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

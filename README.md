
# ace_llm_logic

A logic pipeline that converts natural English into FOL using:

- LLM (to normalize to ACE-compatible form)
- ACE parser with ERG grammar
- LLM (to restore tense/voice/aspect)

## 🔧 Structure

```
ace_llm_logic/
├── python/ace_llm_logic/      # Python source code
├── ace/bin/                   # Place ACE binary here (e.g. ace)
├── ace/grammars/              # Place grammar file here (e.g. erg.dat)
├── tests/                     # Pytest tests
├── requirements.txt
├── pyproject.toml
├── Dockerfile
├── .gitignore
└── README.md
```

## ✅ Usage

```bash
export OPENAI_API_KEY=sk-...
python -m python.ace_llm_logic --file input.txt
```

Or mock mode:

```bash
python -m python.ace_llm_logic --mock
```

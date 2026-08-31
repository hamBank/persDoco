Eliza Chat
==========

A small, test-driven-development (TDD) framework for building an
ELIZA-style CLI chatbot in Python.

## Layout

- `eliza_chat/reflections.py` — pronoun/tense reflection ("I am" -> "you are")
- `eliza_chat/rules.py` — `Rule`: a regex pattern with reflected-substitution responses
- `eliza_chat/engine.py` — `Eliza`: tries rules in order, falls back to defaults
- `eliza_chat/script.py` — the default ELIZA-flavored rule set
- `eliza_chat/cli.py` — REPL loop (`eliza-chat` entry point)
- `tests/` — the test suite (written first; drives the implementation above)

## Running the tests

```
pip install pytest
pytest
```

## Running the chatbot

```
pip install -e .
eliza-chat
```

or, without installing:

```
PYTHONPATH=. python3 -m eliza_chat.cli
```

## Extending the script

Add new `Rule(pattern=..., responses=[...])` entries to
`eliza_chat/script.py`. Patterns are checked in order and the first
match wins, so put more specific patterns before general ones. Use
regex capture groups in the pattern and `{0}`, `{1}`, ... placeholders
in the responses — captured text is pronoun-reflected automatically
before being substituted in.

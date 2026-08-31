Eliza Chat
==========

A small, test-driven-development (TDD) framework for building an
ELIZA-style CLI chatbot in Python. It ships two engines:

- **`eliza_chat.classic`** — a full interpreter for the classic ELIZA
  "DOCTOR" script format (weighted keywords, multi-decomp keys, synonym
  groups, `goto` redirection, the pronoun-reflecting memory queue, and
  pre/post word substitution), driving the real, bundled
  `eliza_chat/data/doctor.txt` script. This is the default engine.
- **`eliza_chat.engine`** — a small, from-scratch `Rule`/`Eliza` engine
  with a tiny built-in script, useful as a simpler starting point for
  writing your own rules. Run it with `--simple`.

## Layout

- `eliza_chat/reflections.py` — pronoun/tense reflection ("I am" -> "you are")
- `eliza_chat/rules.py` — `Rule`: a regex pattern with reflected-substitution responses
- `eliza_chat/engine.py` — `Eliza`: tries rules in order, falls back to defaults
- `eliza_chat/script.py` — the small built-in rule set (`--simple` mode)
- `eliza_chat/classic/script.py` — parser for the classic DOCTOR script format
- `eliza_chat/classic/matching.py` — decomposition-pattern matching (`*` wildcards, `@synonym` tokens)
- `eliza_chat/classic/engine.py` — `ClassicEliza`: the full classic-script interpreter
- `eliza_chat/data/doctor.txt` — the classic ELIZA script (see `NOTICE.md` for provenance/license)
- `eliza_chat/cli.py` — REPL loop (`eliza-chat` entry point)
- `tests/` — the test suite (written first; drives the implementation above),
  including `tests/classic/test_doctor_script.py`, which exercises the
  bundled script directly to cover its keyword, synonym, `goto`, and
  memory patterns

## Running the tests

```
pip install pytest
pytest
```

## Running the chatbot

```
pip install -e .
eliza-chat          # classic DOCTOR script (default)
eliza-chat --simple # small built-in script
```

or, without installing:

```
PYTHONPATH=. python3 -m eliza_chat.cli
```

## Extending the classic script

`eliza_chat/data/doctor.txt` uses the original DOCTOR script format:

```
key: computer 50
  decomp: *
    reasmb: Do computers worry you ?
    reasmb: Why do you mention computers ?
```

- `key: <word> [weight]` — a keyword to watch for (default weight 1);
  the highest-weight keyword found in the input is tried first.
- `decomp: [$] <pattern>` — a decomposition pattern under that key, made
  of literal words, `*` (matches zero or more words), and `@group`
  (matches one word from a `synon:` group). A leading `$` stashes the
  reassembled reply in a memory queue instead of answering immediately,
  to be recalled later when no keyword matches.
- `reasmb: <template>` — a reply template under that decomp, tried
  round-robin; `(N)` inserts the Nth captured group (reflected through
  `post:` substitutions), and `goto <key>` redirects matching to another
  key entirely.
- `pre:`, `post:`, `synon:`, `quit:`, `initial:`, `final:` — word
  substitutions, synonym groups, conversation-ending phrases, and the
  greeting/farewell lines.

Load any script in this format with `eliza_chat.classic.script.load_script`
and drive it with `eliza_chat.classic.engine.ClassicEliza`.

## Extending the simple script

Add new `Rule(pattern=..., responses=[...])` entries to
`eliza_chat/script.py`. Patterns are checked in order and the first
match wins, so put more specific patterns before general ones. Use
regex capture groups in the pattern and `{0}`, `{1}`, ... placeholders
in the responses — captured text is pronoun-reflected automatically
before being substituted in.

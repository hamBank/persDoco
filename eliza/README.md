Eliza Chat
==========

A small, test-driven-development (TDD) framework for building an
ELIZA-style chatbot in Python, presented to end users as
**Vánagandr Jörmungandr** (`eliza_chat.persona.PERSONA_NAME`) — the
underlying engine and module names stay "Eliza"/"ELIZA" in homage to the
original 1966 program. It ships two engines:

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
- `eliza_chat/data/ragebait.txt` — an alternate, deliberately provocative/insulting script for comedic effect (see "Ragebait mode" below)
- `eliza_chat/persona.py` — the display name (`PERSONA_NAME`) shown to end users
- `eliza_chat/cli.py` — REPL loop (`eliza-chat` entry point)
- `eliza_chat/web/app.py` — Flask app (`create_app()`); `eliza-chat-web` entry point
- `eliza_chat/web/templates/index.html` — the browser chat UI
- `tests/` — the test suite (written first; drives the implementation above),
  including `tests/classic/test_doctor_script.py`, which exercises the
  bundled script directly to cover its keyword, synonym, `goto`, and
  memory patterns, and `tests/web/test_app.py`, which drives the Flask
  app with its test client

## Running the tests

```
pip install pytest flask
pytest
```

## Running the chatbot

CLI:

```
pip install -e .
eliza-chat            # classic DOCTOR script (default)
eliza-chat --simple   # small built-in script
eliza-chat --ragebait # deliberately provocative/insulting persona (see below)
```

or, without installing:

```
PYTHONPATH=. python3 -m eliza_chat.cli
```

Web app (a minimal browser chat UI backed by the same classic engine,
with an independent, in-memory conversation per browser session):

```
pip install -e .
eliza-chat-web
```

or, without installing:

```
PYTHONPATH=. python3 -m eliza_chat.web.app
```

then open http://127.0.0.1:5000/. `create_app()` generates a random
session secret at startup if none is set, which is fine for local/dev
use but means sessions (and their in-memory conversation state) don't
survive a restart, and won't be shared across multiple worker
processes — set `app.config["SECRET_KEY"]` explicitly, and move
conversation storage out of the in-process dict, before running this
anywhere beyond a single local process. The web UI's mode picker lets
a visitor choose the classic or ragebait persona before starting.

## Ragebait mode

`eliza_chat/data/ragebait.txt` is the same DOCTOR-format interpreter
driving a different persona: deliberately exaggerated, comedic insults
instead of therapeutic reflection ("Cool story. Nobody asked, but here
we are."). It's for laughs, not harassment — every consumer discloses
that the mode is on up front, since the disclosure is the script's own
`initial:` line (`🔥 RAGEBAIT MODE: ON 🔥 ...`), not something bolted
on by the CLI or web layer. Use `eliza-chat --ragebait` on the CLI, or
pick "ragebait" from the mode picker in the web UI.

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

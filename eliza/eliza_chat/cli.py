import argparse
import importlib.resources
import sys

from .classic.engine import ClassicEliza
from .classic.script import load_script
from .engine import Eliza
from .persona import PERSONA_NAME
from .script import DEFAULT_RESPONSES, DEFAULT_RULES

WELCOME_MESSAGE = f"Hello, I'm {PERSONA_NAME}. How are you feeling today?"
FAREWELL_MESSAGE = "Goodbye. Take care."
PROMPT = "you> "


def _load_bundled_script(filename):
    text = importlib.resources.files("eliza_chat.data").joinpath(filename).read_text()
    return load_script(text)


def build_classic_eliza():
    """Build an Eliza driven by the bundled, classic DOCTOR-format script."""
    return ClassicEliza(_load_bundled_script("doctor.txt"))


def build_ragebait_eliza():
    """Build an Eliza driven by the bundled ragebait script (data/ragebait.txt).

    Same interpreter, deliberately provocative/insulting persona for
    comedic effect. Its script announces the mode is on as the very
    first message, so every consumer gets that disclosure for free.
    """
    return ClassicEliza(_load_bundled_script("ragebait.txt"))


def build_simple_eliza():
    return Eliza(rules=DEFAULT_RULES, defaults=DEFAULT_RESPONSES)


def run_repl(eliza, input_stream=sys.stdin, output_stream=sys.stdout):
    initial = eliza.initial() if hasattr(eliza, "initial") else WELCOME_MESSAGE
    print(initial, file=output_stream)
    while True:
        print(PROMPT, end="", file=output_stream)
        line = input_stream.readline()
        if not line:
            break
        text = line.strip()
        if not text:
            continue
        if hasattr(eliza, "is_farewell") and eliza.is_farewell(text):
            print(FAREWELL_MESSAGE, file=output_stream)
            return
        reply = eliza.respond(text)
        if reply is None:
            final = eliza.final() if hasattr(eliza, "final") else FAREWELL_MESSAGE
            print(final, file=output_stream)
            return
        print(reply, file=output_stream)


def main():
    parser = argparse.ArgumentParser(description="An ELIZA-style CLI chatbot.")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--simple",
        action="store_true",
        help="use the small built-in script instead of the classic DOCTOR script",
    )
    mode.add_argument(
        "--ragebait",
        action="store_true",
        help="deliberately provocative/insulting comedic persona (clearly announced on start)",
    )
    args = parser.parse_args()

    if args.ragebait:
        eliza = build_ragebait_eliza()
    elif args.simple:
        eliza = build_simple_eliza()
    else:
        eliza = build_classic_eliza()
    run_repl(eliza)


if __name__ == "__main__":
    main()

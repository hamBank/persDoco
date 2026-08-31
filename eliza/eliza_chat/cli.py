import sys

from .engine import Eliza
from .script import DEFAULT_RESPONSES, DEFAULT_RULES

WELCOME_MESSAGE = "Hello, I'm Eliza. How are you feeling today?"
FAREWELL_MESSAGE = "Goodbye. Take care."
PROMPT = "you> "


def run_repl(eliza, input_stream=sys.stdin, output_stream=sys.stdout):
    print(WELCOME_MESSAGE, file=output_stream)
    while True:
        print(PROMPT, end="", file=output_stream)
        line = input_stream.readline()
        if not line:
            break
        text = line.strip()
        if not text:
            continue
        if eliza.is_farewell(text):
            print(FAREWELL_MESSAGE, file=output_stream)
            break
        print(eliza.respond(text), file=output_stream)


def main():
    eliza = Eliza(rules=DEFAULT_RULES, defaults=DEFAULT_RESPONSES)
    run_repl(eliza)


if __name__ == "__main__":
    main()

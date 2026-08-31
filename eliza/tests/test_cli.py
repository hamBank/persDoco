import io

from eliza_chat.cli import run_repl
from eliza_chat.engine import Eliza
from eliza_chat.rules import Rule


def make_eliza():
    rules = [Rule(pattern=r"i need (.*)", responses=["Why do you need {0}?"])]
    return Eliza(rules=rules, defaults=["Go on."])


def test_repl_echoes_response_and_exits_on_bye():
    eliza = make_eliza()
    stdin = io.StringIO("i need coffee\nbye\n")
    stdout = io.StringIO()

    run_repl(eliza, input_stream=stdin, output_stream=stdout)

    output = stdout.getvalue()
    assert "Why do you need coffee?" in output


def test_repl_stops_on_end_of_input():
    eliza = make_eliza()
    stdin = io.StringIO("i need sleep\n")
    stdout = io.StringIO()

    run_repl(eliza, input_stream=stdin, output_stream=stdout)

    assert "Why do you need sleep?" in stdout.getvalue()


def test_repl_prints_farewell_message():
    eliza = make_eliza()
    stdin = io.StringIO("bye\n")
    stdout = io.StringIO()

    run_repl(eliza, input_stream=stdin, output_stream=stdout)

    assert "bye" in stdout.getvalue().lower() or "goodbye" in stdout.getvalue().lower()

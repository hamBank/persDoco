import io

from eliza_chat.cli import WELCOME_MESSAGE, build_classic_eliza, run_repl
from eliza_chat.engine import Eliza
from eliza_chat.persona import PERSONA_NAME
from eliza_chat.rules import Rule


def test_welcome_message_uses_the_persona_name():
    assert PERSONA_NAME in WELCOME_MESSAGE


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


def test_build_classic_eliza_loads_the_bundled_doctor_script():
    eliza = build_classic_eliza()
    assert eliza.initial() == "How do you do.  Please tell me your problem."
    assert eliza.respond("bye") is None


def test_repl_works_with_the_classic_engine():
    eliza = build_classic_eliza()
    stdin = io.StringIO("Hello there\nbye\n")
    stdout = io.StringIO()

    run_repl(eliza, input_stream=stdin, output_stream=stdout)

    output = stdout.getvalue()
    assert "How do you do." in output
    assert "Goodbye." in output

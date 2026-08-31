import pytest

from eliza_chat.classic.engine import ClassicEliza
from eliza_chat.classic.script import load_script

BASIC = """
initial: How do you do.  Please tell me your problem.
final: Goodbye.  Thank you for talking to me.
quit: bye
quit: goodbye
pre: i'm i am
post: am are
post: my your
synon: desire want need
synon: family mother father
key: xnone
  decomp: *
    reasmb: I'm not sure I understand you fully.
    reasmb: Please go on.
key: sorry
  decomp: *
    reasmb: Please don't apologise.
key: apologise
  decomp: *
    reasmb: goto sorry
key: i
  decomp: * i @desire *
    reasmb: Why do you want (3) ?
  decomp: * i am *
    reasmb: How long have you been (2) ?
key: my 2
  decomp: $ * my *
    reasmb: Lets discuss further why your (2) .
  decomp: * my * @family *
    reasmb: Tell me more about your family.
  decomp: * my *
    reasmb: Your (2) ?
"""


@pytest.fixture
def eliza():
    return ClassicEliza(load_script(BASIC))


def test_family_specific_decomp_wins_over_generic_my_decomp(eliza):
    reply = eliza.respond("my mother is nice")
    assert reply == "Tell me more about your family."


def test_respond_falls_back_to_xnone_when_no_key_matches(eliza):
    assert eliza.respond("banana smoothie") == "I'm not sure I understand you fully."


def test_respond_cycles_through_reassemblies_in_order(eliza):
    assert eliza.respond("banana smoothie") == "I'm not sure I understand you fully."
    assert eliza.respond("banana smoothie") == "Please go on."
    assert eliza.respond("banana smoothie") == "I'm not sure I understand you fully."


def test_decomp_reflects_captured_pronouns(eliza):
    assert eliza.respond("I am worried") == "How long have you been worried ?"


def test_decomp_uses_synonym_group(eliza):
    assert eliza.respond("I need a vacation") == "Why do you want a vacation ?"


def test_goto_redirects_to_another_key(eliza):
    assert eliza.respond("apologise for the mess") == "Please don't apologise."


def test_pre_substitution_runs_before_matching(eliza):
    assert eliza.respond("I'm worried") == "How long have you been worried ?"


def test_memory_is_saved_and_recalled_later(eliza, monkeypatch):
    monkeypatch.setattr("eliza_chat.classic.engine.random.randrange", lambda n: 0)
    reply = eliza.respond("well my mother is caring")
    assert reply == "Tell me more about your family."

    recalled = eliza.respond("banana smoothie")
    assert recalled == "Lets discuss further why your mother is caring ."


def test_respond_returns_none_on_quit_word(eliza):
    assert eliza.respond("bye") is None
    assert eliza.respond("Goodbye") is None


def test_initial_and_final_messages(eliza):
    assert eliza.initial() == "How do you do.  Please tell me your problem."
    assert eliza.final() == "Goodbye.  Thank you for talking to me."

"""Exercises the bundled ragebait script (data/ragebait.txt).

Same interpreter as doctor.txt, different persona: deliberately
exaggerated, comedic insults instead of therapeutic reflection. The
script's initial greeting is the disclosure that the mode is on, so
every consumer (CLI, web) gets that message for free just by using it.
"""

import importlib.resources

import pytest

from eliza_chat.classic.engine import ClassicEliza
from eliza_chat.classic.script import load_script


@pytest.fixture
def script_text():
    return importlib.resources.files("eliza_chat.data").joinpath("ragebait.txt").read_text()


@pytest.fixture
def eliza(script_text):
    return ClassicEliza(load_script(script_text))


def test_all_synonym_references_are_defined(script_text):
    script = load_script(script_text)
    for key in script.keys.values():
        for decomp in key.decomps:
            for token in decomp.parts:
                if token.startswith("@"):
                    assert token[1:] in script.synonyms, f"undefined synonym {token!r}"


def test_initial_message_discloses_ragebait_mode(eliza):
    assert "RAGEBAIT MODE: ON" in eliza.initial()


def test_desire_produces_a_mocking_reply(eliza):
    reply = eliza.respond("I need a vacation")
    assert reply == "You want a vacation ? Adorable. Manifest harder."


def test_family_topic_gets_roasted(eliza):
    reply = eliza.respond("My mother never listens to me")
    assert reply == "Ah yes, blame the family. Groundbreaking therapy technique."


def test_you_statements_get_thrown_back(eliza):
    reply = eliza.respond("You are annoying")
    assert reply == "I'm annoying ? Says the person who came here to argue with a chatbot."


def test_xnone_fallback_is_dismissive(eliza):
    reply = eliza.respond("xyzzy plugh nonsense")
    assert reply == "Riveting. Truly. Say something interesting for once."


def test_quit_words_still_work(eliza):
    assert eliza.respond("bye") is None
    assert eliza.final() == "Leaving already? Weak. Goodbye."

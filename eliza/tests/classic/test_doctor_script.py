"""Exercises the real, bundled classic ELIZA script (data/doctor.txt).

Each test targets one distinct mechanism the script relies on, so this
file doubles as a coverage check against doctor.txt's conversation
patterns: weighted keys, synonym groups, multi-decomp keys, goto chains,
the memory queue, pre/post substitution, quit words, and the xnone
fallback. Reassembly templates cycle round-robin (see ClassicEliza), so
each fresh fixture instance produces deterministic, exact replies.
"""

import importlib.resources

import pytest

from eliza_chat.classic.engine import ClassicEliza
from eliza_chat.classic.script import load_script


@pytest.fixture
def script_text():
    return importlib.resources.files("eliza_chat.data").joinpath("doctor.txt").read_text()


@pytest.fixture
def eliza(script_text):
    return ClassicEliza(load_script(script_text))


def test_all_goto_targets_exist(script_text):
    script = load_script(script_text)
    for key in script.keys.values():
        for decomp in key.decomps:
            for reasmb in decomp.reasmbs:
                if reasmb[:1] == ["goto"]:
                    target = reasmb[1]
                    assert target in script.keys, f"goto target {target!r} is undefined"


def test_all_synonym_references_are_defined(script_text):
    script = load_script(script_text)
    for key in script.keys.values():
        for decomp in key.decomps:
            for token in decomp.parts:
                if token.startswith("@"):
                    assert token[1:] in script.synonyms, f"undefined synonym {token!r}"


def test_computer_is_a_high_weight_keyword(eliza):
    reply = eliza.respond("Do you think a computer could ever understand me")
    assert reply == "Do computers worry you ?"


def test_desire_synonym_group_covers_want_need_and_desire(eliza):
    replies = [eliza.respond(f"I {verb} a long holiday") for verb in ("want", "need", "desire")]
    assert replies == [
        "What would it mean to you if you got a long holiday ?",
        "Why do you want a long holiday ?",
        "Suppose you got a long holiday soon ?",
    ]


def test_family_synonym_group_redirects_to_family_discussion(eliza):
    reply = eliza.respond("My mother never listens to me")
    assert reply == "Tell me more about your family."


def test_remember_key_tries_its_two_decomps_in_order(eliza):
    first = eliza.respond("I remember my childhood home")
    second = eliza.respond("Do you remember what I said?")
    assert first == "Do you often think of your childhood home ?"
    assert second == "Did you think I would forget what you said? ?"


def test_goto_chain_from_deutsch_to_xforeign(eliza):
    first = eliza.respond("Ich spreche Deutsch")
    second = eliza.respond("Ich spreche Deutsch")
    assert first == "I speak only English."
    assert second == "I told you before, I don't understand German."


def test_memory_queue_saves_my_statements_for_later_recall(eliza, monkeypatch):
    monkeypatch.setattr("eliza_chat.classic.engine.random.randrange", lambda n: 0)

    reply = eliza.respond("My job is boring")
    assert reply == "Your job is boring ?"

    recalled = eliza.respond("xyzzy plugh")
    assert recalled == "Lets discuss further why your job is boring ."


def test_pre_substitution_normalizes_a_synonym_before_matching(eliza):
    reply = eliza.respond("Certainly.")
    assert reply == "You seem to be quite positive."


def test_quit_words_end_the_conversation(eliza):
    assert eliza.respond("bye") is None
    assert eliza.respond("goodbye") is None
    assert eliza.respond("quit") is None


def test_xnone_fallback_when_no_keyword_matches(eliza):
    reply = eliza.respond("qwertyuiop asdfghjkl")
    assert reply == "I'm not sure I understand you fully."


def test_initial_and_final_greetings_present(eliza):
    assert eliza.initial() == "How do you do.  Please tell me your problem."
    assert eliza.final() == "Goodbye.  Thank you for talking to me."

import pytest

from eliza_chat.engine import Eliza
from eliza_chat.rules import Rule


@pytest.fixture
def eliza():
    rules = [
        Rule(pattern=r"i need (.*)", responses=["Why do you need {0}?"]),
        Rule(pattern=r"i am (.*)", responses=["How long have you been {0}?"]),
    ]
    return Eliza(rules=rules, defaults=["Please tell me more.", "Go on."])


def test_engine_uses_first_matching_rule(eliza):
    assert eliza.respond("I need help") == "Why do you need help?"


def test_engine_falls_back_to_default_when_no_rule_matches(eliza, monkeypatch):
    monkeypatch.setattr("eliza_chat.engine.random.choice", lambda seq: seq[0])
    assert eliza.respond("the weather is nice") == "Please tell me more."


def test_engine_tries_rules_in_order():
    rules = [
        Rule(pattern=r"i need (.*)", responses=["specific"]),
        Rule(pattern=r".*", responses=["catch-all"]),
    ]
    eliza = Eliza(rules=rules, defaults=["default"])
    assert eliza.respond("i need coffee") == "specific"
    assert eliza.respond("literally anything else") == "catch-all"


def test_engine_is_stateless_between_calls(eliza):
    first = eliza.respond("I need rest")
    second = eliza.respond("I am tired")
    assert first == "Why do you need rest?"
    assert second == "How long have you been tired?"


def test_engine_requires_at_least_one_default():
    with pytest.raises(ValueError):
        Eliza(rules=[], defaults=[])


def test_engine_exit_keywords_detected(eliza):
    assert eliza.is_farewell("bye") is True
    assert eliza.is_farewell("quit") is True
    assert eliza.is_farewell("goodbye now") is True
    assert eliza.is_farewell("hello") is False

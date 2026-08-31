import pytest

from eliza_chat.rules import Rule


def test_rule_matches_simple_pattern():
    rule = Rule(pattern=r"i need (.*)", responses=["Why do you need {0}?"])
    match = rule.match("I need a vacation")
    assert match is not None


def test_rule_match_is_case_insensitive():
    rule = Rule(pattern=r"hello", responses=["Hi there!"])
    assert rule.match("HELLO") is not None


def test_rule_respond_fills_in_capture_group():
    rule = Rule(pattern=r"i need (.*)", responses=["Why do you need {0}?"])
    response = rule.respond("i need a vacation")
    assert response == "Why do you need a vacation?"


def test_rule_respond_reflects_captured_pronouns():
    rule = Rule(pattern=r"i am (.*)", responses=["How long have you been {0}?"])
    response = rule.respond("i am worried about my exams")
    assert response == "How long have you been worried about your exams?"


def test_rule_with_no_match_returns_none():
    rule = Rule(pattern=r"i need (.*)", responses=["Why do you need {0}?"])
    assert rule.match("hello there") is None


def test_rule_respond_raises_if_no_match():
    rule = Rule(pattern=r"i need (.*)", responses=["Why do you need {0}?"])
    with pytest.raises(ValueError):
        rule.respond("this will not match")


def test_rule_picks_response_from_rng(monkeypatch):
    rule = Rule(pattern=r"hi", responses=["a", "b", "c"])
    monkeypatch.setattr("eliza_chat.rules.random.choice", lambda seq: seq[1])
    assert rule.respond("hi") == "b"

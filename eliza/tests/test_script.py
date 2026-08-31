from eliza_chat.engine import Eliza
from eliza_chat.script import DEFAULT_RULES, DEFAULT_RESPONSES


def test_default_script_loads_into_engine():
    eliza = Eliza(rules=DEFAULT_RULES, defaults=DEFAULT_RESPONSES)
    reply = eliza.respond("I need a friend")
    assert "friend" in reply


def test_default_script_handles_greeting():
    eliza = Eliza(rules=DEFAULT_RULES, defaults=DEFAULT_RESPONSES)
    reply = eliza.respond("hello")
    assert isinstance(reply, str) and reply

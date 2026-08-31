"""A small, classic-ELIZA-flavored default script.

Order matters: more specific patterns are listed before their more
general fallbacks, since Eliza.respond() uses the first matching rule.
"""

from .rules import Rule

DEFAULT_RULES = [
    Rule(
        pattern=r"\bi need (.*)",
        responses=[
            "Why do you need {0}?",
            "Would it really help you to get {0}?",
            "Are you sure you need {0}?",
        ],
    ),
    Rule(
        pattern=r"\bi (?:am|'m) (.*)",
        responses=[
            "How long have you been {0}?",
            "Why do you think you are {0}?",
            "How does being {0} make you feel?",
        ],
    ),
    Rule(
        pattern=r"\bi feel (.*)",
        responses=[
            "Tell me more about feeling {0}.",
            "Do you often feel {0}?",
        ],
    ),
    Rule(
        pattern=r"\bbecause (.*)",
        responses=[
            "Is that the real reason?",
            "What other reasons come to mind?",
        ],
    ),
    Rule(
        pattern=r"\b(?:hi|hello|hey)\b",
        responses=[
            "Hello. How are you feeling today?",
            "Hi there. What's on your mind?",
        ],
    ),
    Rule(
        pattern=r"\bmy (.*)",
        responses=[
            "Tell me more about your {0}.",
            "Why do you say your {0}?",
        ],
    ),
    Rule(
        pattern=r"(.*)\?$",
        responses=[
            "Why do you ask that?",
            "What do you think?",
        ],
    ),
]

DEFAULT_RESPONSES = [
    "Please tell me more.",
    "Go on.",
    "I see. Can you elaborate on that?",
    "How does that make you feel?",
    "Why do you say that?",
]

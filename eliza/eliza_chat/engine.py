import random
import re

FAREWELL_PATTERN = re.compile(r"\b(bye|goodbye|quit|exit)\b", re.IGNORECASE)


class Eliza:
    """Stateless-per-turn ELIZA engine: rules in, response out."""

    def __init__(self, rules, defaults):
        if not defaults:
            raise ValueError("Eliza requires at least one default response")
        self.rules = list(rules)
        self.defaults = list(defaults)

    def respond(self, text):
        for rule in self.rules:
            if rule.match(text):
                return rule.respond(text)
        return random.choice(self.defaults)

    def is_farewell(self, text):
        return FAREWELL_PATTERN.search(text) is not None

import random
import re

from .reflections import reflect


class Rule:
    """A single stimulus-response rule, ELIZA-script style.

    ``pattern`` is a regex matched case-insensitively against the whole
    input. Capture groups are reflected (pronoun-swapped) before being
    substituted into a randomly chosen response template via ``{0}``,
    ``{1}``, etc.
    """

    def __init__(self, pattern, responses):
        if not responses:
            raise ValueError("Rule requires at least one response")
        self.pattern = pattern
        self._regex = re.compile(pattern, re.IGNORECASE)
        self.responses = list(responses)

    def match(self, text):
        return self._regex.search(text)

    def respond(self, text):
        match = self.match(text)
        if match is None:
            raise ValueError(f"'{text}' does not match pattern '{self.pattern}'")
        reflected_groups = [reflect(group) for group in match.groups()]
        template = random.choice(self.responses)
        return template.format(*reflected_groups)

import re

# Pairs are intentionally one-directional per lookup; both directions are
# listed explicitly so "i am" <-> "you are" reflects correctly either way.
REFLECTIONS = {
    "i": "you",
    "me": "you",
    "my": "your",
    "mine": "yours",
    "myself": "yourself",
    "am": "are",
    "you": "I",
    "your": "my",
    "yours": "mine",
    "yourself": "myself",
    "are": "am",
    "i'm": "you're",
    "i've": "you've",
    "i'll": "you'll",
    "i'd": "you'd",
}

_WORD_RE = re.compile(r"[A-Za-z']+|[^A-Za-z']+")


def reflect(text):
    parts = _WORD_RE.findall(text)
    reflected = []
    for part in parts:
        lower = part.lower()
        if lower in REFLECTIONS:
            reflected.append(REFLECTIONS[lower])
        else:
            reflected.append(part)
    return "".join(reflected)

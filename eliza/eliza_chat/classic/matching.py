"""Decomposition-pattern matching for the classic ELIZA script format.

A decomposition pattern is a list of tokens, each one of:

- ``"*"``      — a wildcard matching zero or more words
- ``"@name"``  — matches a single word that belongs to the ``name``
                 synonym group (see :mod:`eliza_chat.classic.script`)
- anything else — a literal word, matched case-insensitively

Matching a pattern against a sentence (a list of words) yields one capture
group per wildcard/synonym token, in the order those tokens appear in the
pattern — mirroring the ``(1)``, ``(2)``, ... placeholders used in the
script's reassembly templates.
"""


def match_decomp(parts, words, synonyms):
    """Return the list of captured groups, or None if the pattern doesn't match."""
    return _match(parts, words, synonyms)


def _match(parts, words, synonyms):
    if not parts and not words:
        return []
    if not parts:
        return None
    if not words and parts != ["*"]:
        return None

    token = parts[0]

    if token == "*":
        for take in range(len(words), -1, -1):
            rest = _match(parts[1:], words[take:], synonyms)
            if rest is not None:
                return [words[:take]] + rest
        return None

    if token.startswith("@"):
        if not words:
            return None
        group = token[1:]
        members = synonyms.get(group)
        if members is None:
            raise ValueError(f"Unknown synonym root {group!r}")
        if words[0].lower() not in members:
            return None
        rest = _match(parts[1:], words[1:], synonyms)
        if rest is None:
            return None
        return [[words[0]]] + rest

    if not words or token.lower() != words[0].lower():
        return None
    return _match(parts[1:], words[1:], synonyms)

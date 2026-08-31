"""Parser for the classic ELIZA "DOCTOR" script format.

The format (one directive per line, ``tag: content``) supports:

- ``initial:`` / ``final:``  — greeting / farewell lines
- ``quit:``                  — an exact phrase that ends the conversation
- ``pre:``  / ``post:``       — word substitutions applied before matching
                                 (pre) and to captured text (post)
- ``synon:``                  — a synonym group, referenced as ``@name``
- ``key:``                    — a keyword, with an optional weight
- ``decomp:``                 — a decomposition pattern under the current key
                                 (a leading ``$`` marks it as memory-only)
- ``reasmb:``                 — a reassembly template under the current decomp
"""


class Decomp:
    def __init__(self, parts, save, reasmbs=None):
        self.parts = parts
        self.save = save
        self.reasmbs = reasmbs if reasmbs is not None else []
        self.next_index = 0


class Key:
    def __init__(self, word, weight, decomps=None):
        self.word = word
        self.weight = weight
        self.decomps = decomps if decomps is not None else []


class Script:
    def __init__(self):
        self.initials = []
        self.finals = []
        self.quits = []
        self.pres = {}
        self.posts = {}
        self.synonyms = {}
        self.keys = {}

    def synonym_members(self, name):
        if name not in self.synonyms:
            raise ValueError(f"Unknown synonym root {name!r}")
        return self.synonyms[name]


def load_script(text):
    script = Script()
    key = None
    decomp = None

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        tag, _, content = line.partition(":")
        tag = tag.strip()
        content = content.strip()

        if tag == "initial":
            script.initials.append(content)
        elif tag == "final":
            script.finals.append(content)
        elif tag == "quit":
            script.quits.append(content)
        elif tag == "pre":
            parts = content.split()
            script.pres[parts[0]] = parts[1:]
        elif tag == "post":
            parts = content.split()
            script.posts[parts[0]] = parts[1:]
        elif tag == "synon":
            parts = content.split()
            script.synonyms[parts[0]] = parts
        elif tag == "key":
            parts = content.split()
            word = parts[0]
            weight = int(parts[1]) if len(parts) > 1 else 1
            key = Key(word, weight)
            script.keys[word] = key
        elif tag == "decomp":
            parts = content.split()
            save = False
            if parts and parts[0] == "$":
                save = True
                parts = parts[1:]
            decomp = Decomp(parts, save)
            key.decomps.append(decomp)
        elif tag == "reasmb":
            decomp.reasmbs.append(content.split())
        else:
            raise ValueError(f"Unknown script directive {tag!r}")

    return script

import random
import re

from .matching import match_decomp

_PUNCT_RE = re.compile(r"\s*([.,;])+\s*")
_PAREN_REF_RE = re.compile(r"^\((\d+)\)$")


class ClassicEliza:
    """Interprets a classic ELIZA "DOCTOR"-format :class:`Script`.

    Faithful to the reference algorithm: keys are tried highest-weight
    first, decompositions within a key are tried in order, ``goto``
    reassemblies redirect to another key, ``$``-flagged decompositions are
    stashed in a memory queue instead of answered immediately, and
    reassembly templates cycle round-robin rather than at random.
    """

    def __init__(self, script):
        self.script = script
        self.memory = []

    def initial(self):
        return random.choice(self.script.initials)

    def final(self):
        return random.choice(self.script.finals)

    def respond(self, text):
        if text.lower() in self.script.quits:
            return None

        words = self._tokenize(text)
        words = self._substitute(words, self.script.pres)

        keys = [
            self.script.keys[word.lower()]
            for word in words
            if word.lower() in self.script.keys
        ]
        keys.sort(key=lambda key: -key.weight)

        output = None
        for key in keys:
            output = self._match_key(words, key)
            if output:
                break

        if not output:
            if self.memory:
                index = random.randrange(len(self.memory))
                output = self.memory.pop(index)
            else:
                output = self._next_reassembly(self.script.keys["xnone"].decomps[0])

        return " ".join(output)

    @staticmethod
    def _tokenize(text):
        text = _PUNCT_RE.sub(lambda m: f" {m.group(1)} ", text)
        return [word for word in text.split(" ") if word]

    @staticmethod
    def _substitute(words, table):
        output = []
        for word in words:
            output.extend(table.get(word.lower(), [word]))
        return output

    @staticmethod
    def _next_reassembly(decomp):
        index = decomp.next_index
        reasmb = decomp.reasmbs[index % len(decomp.reasmbs)]
        decomp.next_index = index + 1
        return reasmb

    def _match_key(self, words, key):
        for decomp in key.decomps:
            groups = match_decomp(decomp.parts, words, self.script.synonyms)
            if groups is None:
                continue

            groups = [self._substitute(group, self.script.posts) for group in groups]
            reasmb = self._next_reassembly(decomp)

            if reasmb[:1] == ["goto"]:
                target = self.script.keys[reasmb[1]]
                return self._match_key(words, target)

            output = self._reassemble(reasmb, groups)
            if decomp.save:
                self.memory.append(output)
                continue
            return output
        return None

    @staticmethod
    def _reassemble(reasmb, groups):
        output = []
        for word in reasmb:
            match = _PAREN_REF_RE.match(word)
            if not match:
                output.append(word)
                continue
            index = int(match.group(1))
            insert = groups[index - 1]
            for punct in (",", ".", ";"):
                if punct in insert:
                    insert = insert[: insert.index(punct)]
            output.extend(insert)
        return output

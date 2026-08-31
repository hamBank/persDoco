from eliza_chat.classic.matching import match_decomp


def test_wildcard_only_captures_everything():
    result = match_decomp(["*"], ["I", "need", "help"], synonyms={})
    assert result == [["I", "need", "help"]]


def test_literal_word_must_match_case_insensitively():
    result = match_decomp(["Hello"], ["hello"], synonyms={})
    assert result == []


def test_literal_mismatch_fails():
    result = match_decomp(["hello"], ["goodbye"], synonyms={})
    assert result is None


def test_wildcards_capture_text_around_a_literal():
    result = match_decomp(
        ["*", "my", "*"],
        ["well", "my", "mother", "is", "nice"],
        synonyms={},
    )
    assert result == [["well"], ["mother", "is", "nice"]]


def test_synonym_token_matches_any_member_and_captures_the_word():
    result = match_decomp(
        ["*", "i", "@desire", "*"],
        ["i", "need", "a", "vacation"],
        synonyms={"desire": ["desire", "want", "need"]},
    )
    assert result == [[], ["need"], ["a", "vacation"]]


def test_no_match_returns_none():
    result = match_decomp(["*", "my", "*"], ["hello", "there"], synonyms={})
    assert result is None


def test_trailing_wildcard_matches_empty_remainder():
    result = match_decomp(["hi", "*"], ["hi"], synonyms={})
    assert result == [[]]

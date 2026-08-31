import pytest

from eliza_chat.classic.script import load_script

SAMPLE = """
initial: How do you do.  Please tell me your problem.
final: Goodbye.  Thank you for talking to me.
quit: bye
quit: goodbye
pre: dont don't
pre: i'm i am
post: am are
post: my your
synon: desire want need
key: xnone
  decomp: *
    reasmb: I'm not sure I understand you fully.
    reasmb: Please go on.
key: sorry
  decomp: *
    reasmb: goto xnone
key: remember 5
  decomp: * i remember *
    reasmb: Do you often think of (2) ?
  decomp: * do you remember *
    reasmb: Did you think I would forget (2) ?
key: my 2
  decomp: $ * my *
    reasmb: Lets discuss further why your (2) .
  decomp: * my *
    reasmb: Your (2) ?
"""


def test_parses_initial_and_final():
    script = load_script(SAMPLE)
    assert script.initials == ["How do you do.  Please tell me your problem."]
    assert script.finals == ["Goodbye.  Thank you for talking to me."]


def test_parses_quit_words():
    script = load_script(SAMPLE)
    assert script.quits == ["bye", "goodbye"]


def test_parses_pre_substitutions_as_word_lists():
    script = load_script(SAMPLE)
    assert script.pres["dont"] == ["don't"]
    assert script.pres["i'm"] == ["i", "am"]


def test_parses_post_substitutions():
    script = load_script(SAMPLE)
    assert script.posts["am"] == ["are"]
    assert script.posts["my"] == ["your"]


def test_parses_synonyms_including_the_root_word():
    script = load_script(SAMPLE)
    assert script.synonyms["desire"] == ["desire", "want", "need"]


def test_parses_keys_with_default_and_explicit_weight():
    script = load_script(SAMPLE)
    assert script.keys["xnone"].weight == 1
    assert script.keys["remember"].weight == 5
    assert script.keys["my"].weight == 2


def test_parses_multiple_decomps_per_key_in_order():
    script = load_script(SAMPLE)
    remember = script.keys["remember"]
    assert len(remember.decomps) == 2
    assert remember.decomps[0].parts == ["*", "i", "remember", "*"]
    assert remember.decomps[1].parts == ["*", "do", "you", "remember", "*"]


def test_parses_reassemblies_as_word_lists():
    script = load_script(SAMPLE)
    decomp = script.keys["xnone"].decomps[0]
    assert decomp.reasmbs[0] == ["I'm", "not", "sure", "I", "understand", "you", "fully."]
    assert decomp.reasmbs[1] == ["Please", "go", "on."]


def test_parses_memory_flag_from_dollar_prefix():
    script = load_script(SAMPLE)
    my_key = script.keys["my"]
    assert my_key.decomps[0].save is True
    assert my_key.decomps[0].parts == ["*", "my", "*"]
    assert my_key.decomps[1].save is False


def test_unknown_synonym_reference_raises_when_used():
    script = load_script(SAMPLE)
    with pytest.raises(ValueError):
        script.synonym_members("nonexistent")

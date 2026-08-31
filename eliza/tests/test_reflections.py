from eliza_chat.reflections import reflect


def test_reflect_swaps_first_and_second_person():
    assert reflect("i am") == "you are"


def test_reflect_swaps_possessives():
    assert reflect("my mother") == "your mother"


def test_reflect_is_case_insensitive_on_input():
    assert reflect("I Am Your Friend") == "you are my Friend"


def test_reflect_leaves_unmapped_words_untouched():
    assert reflect("the sky is blue") == "the sky is blue"


def test_reflect_only_matches_whole_words():
    # "mine" contains "i" but must not be corrupted into "myne" or similar
    assert reflect("mine") == "yours"
    assert reflect("imagine") == "imagine"

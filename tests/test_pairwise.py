from sparkles import pairwise


def test_gives_me_pairs():
    assert list(pairwise("AAB")) == [("A", "A"), ("A", "B")]

from sparkles import lookup


def test_accepts_iterable_and_key():
    lookup([], lambda x: x)


def test_empty_lookup_returns_empty_dict():
    assert lookup([], lambda x: x) == {}


def test_single_lookup_returns_single_dict():
    assert lookup([1], lambda x: x) == {1: 1}

import pytest

from sparkles import sorted_groupby


def test_takes_an_iterable_and_a_key():
    sorted_groupby(iterable="abcd", key=lambda x: x)


def test_throws_exception_if_iterable_is_not_iterable():
    with pytest.raises(TypeError):
        sorted_groupby(iterable=1, key=lambda x: x)


def test_groups_unsorted():
    assert dict(sorted_groupby(iterable="aba", key=lambda x: x, value=list)) == {
        "a": ["a", "a"],
        "b": ["b"],
    }

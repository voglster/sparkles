from sparkles import parse_csl


def test_single_item():
    assert parse_csl("test") == ["test"]


def test_no_items():
    assert parse_csl("") == []


def test_2_items():
    assert parse_csl("bob,villa") == ["bob", "villa"]


def test_lowercase():
    assert parse_csl("Bob") == ["bob"]


def test_no_lowercase():
    assert parse_csl("Bob", lower=False) == ["Bob"]

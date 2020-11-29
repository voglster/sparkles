from sparkles import to_dicts


def test_to_dicts_returns_empty_list_when_empty():
    assert to_dicts(None) == []


def test_to_dicts_returns_empty_list_when_only_one_row():
    assert to_dicts([["a", "b"]]) == []


def test_to_dicts_returns_one_row_when_header_and_data_present():
    assert to_dicts([["a", "b"], [1, 2]]) == [{"a": 1, "b": 2}]


def test_to_dicts_handles_iterable_instead_of_list():
    gen = (x for x in [["a", "b"], [1, 2]])

    assert to_dicts(gen) == [{"a": 1, "b": 2}]

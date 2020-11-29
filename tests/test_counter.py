import pytest
from sparkles import counter


@pytest.fixture
def a_counter():
    return counter(12, 6)


def test_first_counter_is_start():
    q = next(counter(12))
    assert q == 12


def test_second_counter_is_start_plus_step():
    start = 5
    step = 12
    expected = start + step
    c = counter(start, step)
    next(c)
    q = next(c)
    assert q == expected

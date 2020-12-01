import pytest
from sparkles import parse_float, parse_int
from sparkles.parsing import lower_string

valid_float_inputs = [
    ("3,000.00", 3000.0),
    ("-", 0.0),
    (" -", 0.0),
    ("- ", 0.0),
    (" 3,000.00", 3000.0),
    (" 3,000.00 ", 3000.0),
    (" $3,000.00 ", 3000.0),
]


@pytest.mark.parametrize("float_str_value,expected", valid_float_inputs)
def test_parsing_valid_floats(float_str_value, expected):
    assert parse_float(float_str_value) == expected


invalid_float_inputs = [
    "A3,000.00",
    " MIKE ",
]


@pytest.mark.parametrize("float_str_value", invalid_float_inputs)
def test_parsing_invalid_floats_raises(float_str_value):
    with pytest.raises(ValueError):
        parse_float(float_str_value)


valid_int_inputs = [
    ("3,000.00", 3000),
    ("-", 0),
    (" -", 0),
    ("- ", 0),
    (" 3,000.00", 3000),
    (" 3,000.00 ", 3000),
    (" $3,000.00 ", 3000),
]


@pytest.mark.parametrize("int_str_value,expected", valid_int_inputs)
def test_parsing_valid_ints(int_str_value, expected):
    int_value = parse_int(int_str_value)
    assert int_value == expected
    assert isinstance(int_value, int), "int_value response is not an int"


invalid_int_inputs = [
    "A3,000.50",
    " MIKE ",
    "3000.5",
]


@pytest.mark.parametrize("int_str_value", invalid_int_inputs)
def test_parsing_invalid_floats_raises_value_error(int_str_value):
    with pytest.raises(ValueError):
        parse_int(int_str_value)


def test_string_lower_sends_values_error_on_none():
    with pytest.raises(ValueError):
        lower_string(None)


valid_string_lower_inputs = [
    ("TEST", "test"),
    (" TEST", "test"),
    ("TEST ", "test"),
    ("test", "test"),
]


@pytest.mark.parametrize("string_to_lower, expected", valid_string_lower_inputs)
def test_string_lower_valid_values(string_to_lower, expected):
    pass

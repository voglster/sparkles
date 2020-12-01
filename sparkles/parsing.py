def parse_float(value: str) -> float:
    value = value.strip()
    if value == "-":
        return 0.0

    return float(value.replace(",", "").replace("$", ""))


def parse_int(value: str):
    float_value = parse_float(value)
    if not float_value.is_integer():
        raise ValueError(f"{value} is not an integer")
    return int(float_value)


def lower_string(value: str):
    if value is None:
        raise ValueError("Lower string called on None")
    return value.strip().lower()

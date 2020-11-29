from typing import Iterable


def split_header_and_data(rows: Iterable[list]):
    row_iter = iter(rows)
    header = next(row_iter)
    return header, row_iter


def list_of_dicts(header, data):
    return [dict(zip(header, row)) for row in data]


def to_dicts(ds):
    if not ds:
        return []
    header, data = split_header_and_data(ds)
    return list_of_dicts(header, data)

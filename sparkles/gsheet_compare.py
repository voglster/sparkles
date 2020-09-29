from pprint import pprint
from time import sleep

from sparkles.google_sheet import get_book


def get_worksheet_names(book):
    return {sheet.title for sheet in book}


def foo(sheet_names, master, target):
    pass


def run(master_sheet_key, target_sheet_key):
    master_book = get_book(master_sheet_key)
    target_book = get_book(target_sheet_key)

    master_sheet_names = get_worksheet_names(master_book)
    target_sheet_names = get_worksheet_names(target_book)

    missing_sheets = master_sheet_names - target_sheet_names

    ret = {}
    for name in master_sheet_names.intersection(target_sheet_names):
        print(f"Doing {name}")
        master_ws = master_book.worksheet(name)
        target_ws = target_book.worksheet(name)
        column_diff = set(master_ws.row_values(1)) - set(target_ws.row_values(1))
        print(column_diff)
        ret[name] = column_diff
        sleep(10)

    return {"missing_sheets": missing_sheets, "missing_columns": ret}


if __name__ == "__main__":
    pprint(
        run(
            "1IBGy2cY5q79en7OEs1b0QoAZlTaLrw6KoAF-O75XnSE",
            "16L2EQ4zA9d2FrEk7vdt3xiVclZFr1mN-lOFSv6lmSBQ",
        )
    )

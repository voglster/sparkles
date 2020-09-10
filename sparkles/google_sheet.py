import gspread
from gspread import WorksheetNotFound
from loguru import logger
from oauth2client.service_account import ServiceAccountCredentials
import logging


class Config:
    google_credentials_file = "service_account.json"
    default_google_sheet_key = ""
    ignored_sheets = ["Results", "Status"]


config = Config()


def ignored_sheets():
    return [tab_name.casefold() for tab_name in config.ignored_sheets]


def auth(credential_file=config.google_credentials_file):
    from pathlib import Path

    credential_file = Path(__file__).parent.parent / credential_file
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
    ]
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        credential_file, scope
    )
    return gspread.authorize(credentials)


def get_book(sheet_key, gc=None):
    if gc is None:
        gc = auth()
    logging.info(f"Opening Google Sheet {sheet_key}")
    book = gc.open_by_key(sheet_key)
    logging.info(f"Google Sheet Title is {book.title}")
    return book


def data_sheets(book):
    """Lists all worksheets that aren't in ignored sheets"""
    for worksheet in book:
        title = worksheet.title
        if title.casefold() in ignored_sheets():
            continue
        yield worksheet


def clean_worksheet_data(worksheet, log):
    log(f"Loading sheet {worksheet.title}")
    data = worksheet.get_all_values()
    data[0] = [str(col).strip() for col in data[0]]  # strip whitespace on column names
    return data


def to_dataset(book, log=lambda x: None):
    log("Loading sheets")
    return {
        worksheet.title: clean_worksheet_data(worksheet, log)
        for worksheet in data_sheets(book)
    }


def data_set(sheet_key, log=lambda x: None):
    book = get_book(sheet_key)
    return book.title, to_dataset(book, log)


def get_sheet(book, name):

    try:
        return book.worksheet(name)
    except WorksheetNotFound:
        logger.exception(
            f"Tried to load a sheet named: {name} but there is not sheet named that here: {book.url}"
        )
        return


def get_sheet_data(name, book=None):
    book = book or get_book(config.default_google_sheet_key)
    if sheet := get_sheet(book, name):
        return sheet.get_all_records()
    return []

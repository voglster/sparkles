import logging
import os
from pathlib import Path

from gspread import WorksheetNotFound, authorize
from loguru import logger
from oauth2client.service_account import ServiceAccountCredentials

from .file_utils import find_file_above


class Config:
    google_credentials_file = "service_account.json"
    default_google_sheet_key = ""
    ignored_sheets = ["Results", "Status"]


config = Config()


def ignored_sheets():
    return [tab_name.casefold() for tab_name in config.ignored_sheets]


def auth(credential_file=None):
    credential_file = credential_file or config.google_credentials_file
    path = absolute_path_for(credential_file)
    logger.info(f"Authorizing google with credential file {path}")
    credentials = load_gspread_credentials(path)
    return authorize(credentials)


def load_gspread_credentials(absolute_path):
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
    ]
    return ServiceAccountCredentials.from_json_keyfile_name(absolute_path, scope)


def absolute_path_for(original_credential_file):
    if os.sep in original_credential_file:
        credential_file = Path(__file__).parent.parent / original_credential_file
    else:
        credential_file = find_file_above(original_credential_file, os.getcwd())

    if not credential_file:
        raise Exception(
            f"Could not find a credential file {original_credential_file} above {os.getcwd()}"
        )
    return credential_file


def get_book(sheet_key, gc=None):
    if gc is None:
        gc = auth()
    elif type(gc) == str:
        gc = auth(gc)
    logging.info(f"Opening Google Sheet {sheet_key}")
    book = gc.open_by_key(sheet_key)
    logging.info(f"Google Sheet Title is {book.title}")
    return book


def get_fast_book(sheet_key, gc=None):
    if gc is None:
        gc = auth()
    elif type(gc) == str:
        gc = auth(gc)
    logging.info(f"Opening Google Sheet {sheet_key}")
    from .fast_gsheet import FastGSheet

    book = FastGSheet(sheet_key, gc)
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

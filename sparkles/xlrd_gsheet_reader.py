from io import BytesIO

import xlrd
import requests
from .google_sheet import auth


def google_url_from_sheet_key(sheet_key):
    return (
        f"https://www.googleapis.com/drive/v3/files/{sheet_key}/export?"
        f"mimeType=application%2Fvnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


def download_sheet_from_google_docs(sheet_key, auth):
    access_token = get_gspread_access_token(auth)
    url = google_url_from_sheet_key(sheet_key)
    res = requests.get(url, headers={"Authorization": f"Bearer {access_token}"})
    return res.content


def get_gspread_access_token(auth):
    client = auth or auth()
    if not client.auth.token:
        client.login()
    return client.auth.token


def parse_xls_workbook(content):
    workbook = xlrd.open_workbook(file_contents=BytesIO(content).read())
    return {sheet.name: list(data_rows(sheet)) for sheet in workbook.sheets()}


def data_rows(sheet):
    for row in sheet.get_rows():
        if row[0].ctype == xlrd.XL_CELL_EMPTY:
            break
        yield [parse_excel_cell(column) for column in row]


def parse_excel_date(value):
    return xlrd.xldate.xldate_as_datetime(value, 0).isoformat()


parsers = {
    xlrd.XL_CELL_BOOLEAN: lambda x: "True" if x else "False",
    xlrd.XL_CELL_DATE: parse_excel_date,
    xlrd.XL_CELL_NUMBER: lambda v: str(int(v) if v.is_integer() else v),
    xlrd.XL_CELL_TEXT: lambda v: v,
    xlrd.XL_CELL_EMPTY: lambda v: v,
    xlrd.XL_CELL_BLANK: lambda v: v,
    xlrd.XL_CELL_ERROR: lambda v: "",
}


def parse_excel_cell(column: xlrd.sheet.Cell):
    parser = parsers[column.ctype]
    return parser(column.value)

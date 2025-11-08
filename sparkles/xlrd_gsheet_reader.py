from datetime import datetime
from io import BytesIO

import openpyxl
import requests


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
    workbook = openpyxl.load_workbook(BytesIO(content), data_only=True)
    return {sheet.title: list(data_rows(sheet)) for sheet in workbook.worksheets}


def data_rows(sheet):
    for row in sheet.iter_rows(values_only=False):
        if row[0].value is None:
            break
        yield [parse_excel_cell(cell) for cell in row]


def parse_excel_cell(cell):
    value = cell.value
    if value is None:
        return ""
    if isinstance(value, bool):
        return "True" if value else "False"
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, (int, float)):
        return str(int(value) if isinstance(value, float) and value.is_integer() else value)
    return str(value)

from .xlrd_gsheet_reader import (
    download_sheet_from_google_docs,
    parse_xls_workbook,
)
from .data_utils import to_dicts


class FastGSheet:
    def __init__(self, sheet_key, auth):
        content = download_sheet_from_google_docs(sheet_key, auth)
        self.data = {
            key: FastSheet(value) for key, value in parse_xls_workbook(content).items()
        }

    def worksheet(self, name):
        return self.data[name]


class FastSheet:
    def __init__(self, data):
        self.data = data

    def get_all_records(self, numericise_ignore=None):
        return to_dicts(self.data)

    def get_all_values(self, numericise_ignore=None):
        return self.data

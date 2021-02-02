import pytest

from sparkles import google_sheet


def test_file_not_found_exception():
    with pytest.raises(FileNotFoundError):
        google_sheet.absolute_path_for("ZZZZZZZ.ZZZ")

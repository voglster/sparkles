import pytest
from sparkles import logged_user


class MockLogger:
    last_line = None

    def info(self, message):
        self.last_line = message


@pytest.fixture
def logger():
    return MockLogger()


@pytest.fixture
def local_logged_user(logger):
    return logged_user(logger=logger)


@pytest.fixture
def logged_do_nothing(local_logged_user):
    @local_logged_user
    def do_nothing(*args, **kwargs):
        pass

    return do_nothing


class MockUser:
    username = "mock"


@pytest.fixture
def mock_user():
    return MockUser()


def test_logged_user_returns_a_function(local_logged_user):
    assert callable(local_logged_user)


def test_logged_user_doesnt_fail_when_no_user(logged_do_nothing):
    logged_do_nothing()


def test_logged_user_logs_a_line_when_method_called(logger, logged_do_nothing):
    assert logger.last_line is None
    logged_do_nothing()
    assert logger.last_line


def test_logged_user_logs_include_username(mock_user, logger, logged_do_nothing):
    logged_do_nothing(current_user=mock_user)
    assert "mock" in logger.last_line

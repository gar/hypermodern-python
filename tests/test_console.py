import click.testing
import pytest
import requests

from hypermodern_python import console


@pytest.fixture
def runner():
    return click.testing.CliRunner()


@pytest.fixture
def mock_requests_get(mocker):
    mock = mocker.patch("requests.get")
    mock.return_value.__enter__.return_value.json.return_value = {
        "title": "Lorem Ipsum",
        "extract": "Lorem ipsum dolor sit amet",
    }
    return mock


@pytest.fixture
def en_locale_mock(mocker):
    mock = mocker.patch("locale.getlocale")
    mock.return_value = ("en_US",)
    return mock


def test_main_succeeds(runner, mock_requests_get):
    result = runner.invoke(console.main)
    assert result.exit_code == 0


def test_title_is_in_result(runner, mock_requests_get):
    result = runner.invoke(console.main)
    assert "Lorem Ipsum" in result.output


def test_main_uses_locale_by_default(runner, mock_requests_get, en_locale_mock):
    runner.invoke(console.main)
    args, _ = mock_requests_get.call_args
    assert "en.wikipedia.org" in args[0]


def test_lang_can_be_overridden(runner, mock_requests_get, en_locale_mock):
    runner.invoke(console.main, ["--lang", "es"])
    args, _ = mock_requests_get.call_args
    assert "es.wikipedia.org" in args[0]


def test_main_fails_when_http_error(runner, mock_requests_get):
    mock_requests_get.side_effect = requests.RequestException
    result = runner.invoke(console.main)
    assert "Error" in result.output
    assert result.exit_code == 1

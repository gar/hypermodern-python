import click.testing
import pytest
import requests

from hypermodern_python import console


@pytest.fixture
def runner():
    return click.testing.CliRunner()


@pytest.fixture
def mock_locale(mocker):
    mock = mocker.patch("locale.getlocale")
    mock.return_value = ("en_US",)
    return mock


@pytest.fixture
def mock_wikipedia_random_page(mocker):
    return mocker.patch("hypermodern_python.wikipedia.random_page")


def test_main_succeeds(runner, mock_requests_get):
    result = runner.invoke(console.main)
    assert result.exit_code == 0


def test_title_is_in_result(runner, mock_requests_get):
    result = runner.invoke(console.main)
    assert "Lorem Ipsum" in result.output


def test_main_uses_locale_by_default(runner, mock_wikipedia_random_page, mock_locale):
    runner.invoke(console.main)
    mock_wikipedia_random_page.assert_called_with(language="en")


def test_lang_can_be_overridden(runner, mock_wikipedia_random_page, mock_locale):
    runner.invoke(console.main, ["--language=es"])
    mock_wikipedia_random_page.assert_called_with(language="es")


def test_main_fails_when_http_error(runner, mock_requests_get):
    mock_requests_get.side_effect = requests.RequestException
    result = runner.invoke(console.main)
    assert "Error" in result.output
    assert result.exit_code == 1

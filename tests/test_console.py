import click.testing
import pytest

from hypermodern_python import console


@pytest.fixture
def runner():
    return click.testing.CliRunner()


def test_main_succeeds(runner):
    result = runner.invoke(console.main)
    assert result.exit_code == 0


def test_main_failes_when_bad_lang_given(runner):
    result = runner.invoke(console.main, ["--lang", "foobar"])
    assert result.exit_code == 1

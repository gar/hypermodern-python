import locale
import textwrap

import click
import requests

from . import __version__, wikipedia

LOCALE_LANG = locale.getlocale()[0].split("_")[0]


@click.command()
@click.version_option(version=__version__)
@click.option(
    "--lang",
    default=LOCALE_LANG,
    help="Use Wikipedia edition for a given language code",
)
def main(lang):
    """The hypermodern Python project."""

    try:
        data = wikipedia.random_page(lang)

        title = data["title"]
        extract = data["extract"]

        click.secho(title, fg="green")
        click.echo(textwrap.fill(extract))

    except requests.RequestException as error:
        message = str(error)
        raise click.ClickException(message)

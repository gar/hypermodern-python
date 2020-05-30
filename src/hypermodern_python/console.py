import locale
import textwrap

import click

from . import __version__, wikipedia

LOCALE_LANG = locale.getlocale()[0].split("_")[0]


@click.command()
@click.version_option(version=__version__)
@click.option(
    "--language",
    "--l",
    default=LOCALE_LANG,
    help="Language edition of Wikipedia",
    metavar="LANG",
    show_default=True,
)
def main(language):
    """The hypermodern Python project."""

    data = wikipedia.random_page(language=language)

    title = data["title"]
    extract = data["extract"]

    click.secho(title, fg="green")
    click.echo(textwrap.fill(extract))

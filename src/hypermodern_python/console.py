import locale
import textwrap

import click
import requests

from . import __version__

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

    api_url = f"https://{lang}.wikipedia.org/api/rest_v1/page/random/summary"
    headers = {"User-Agent": "https://github.com/gar"}

    try:
        with requests.get(api_url, headers=headers) as response:
            response.raise_for_status()
            data = response.json()

        title = data["title"]
        extract = data["extract"]

        click.secho(title, fg="green")
        click.echo(textwrap.fill(extract))

    except Exception as err:
        click.secho(f"failed with error {err}", fg="red")
        exit(1)

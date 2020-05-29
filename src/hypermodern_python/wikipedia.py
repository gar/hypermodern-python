import requests


def random_page(lang):
    api_url = f"https://{lang}.wikipedia.org/api/rest_v1/page/random/summary"
    headers = {"User-Agent": "https://github.com/gar"}

    with requests.get(api_url, headers=headers) as response:
        response.raise_for_status()
        return response.json()

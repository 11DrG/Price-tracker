import os
import re
import requests
from pages.base_page import BasePage

_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
}

def _build_url(url):
    api_key = os.getenv("SCRAPER_API_KEY")
    if api_key:
        return f"http://api.scraperapi.com?api_key={api_key}&url={url}"
    return url


class EmagProductPage(BasePage):
    site_name = "eMAG"

    def __init__(self, page):
        super().__init__(page)
        self._html = None

    def open(self, url):
        response = requests.get(_build_url(url), headers=_HEADERS, timeout=60)
        response.raise_for_status()
        self._html = response.text

    def get_current_price(self):
        match = re.search(
            r'data-test="main-price">(\d+)<sup><small[^>]*>[^<]*</small>(\d+)</sup>',
            self._html,
        )
        if not match:
            raise ValueError("Price element not found in eMAG response")
        return float(f"{match.group(1)}.{match.group(2)}")

    def get_original_price(self, current_price):
        match = re.search(
            r'<s>(\d+)<sup><small[^>]*>[^<]*</small>(\d+)</sup>',
            self._html,
        )
        if not match:
            return None
        original = float(f"{match.group(1)}.{match.group(2)}")
        if original < current_price:
            return None
        return original

    def screenshot_on_failure(self, url):
        return None

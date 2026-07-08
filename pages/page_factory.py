from pages.emag_page import EmagProductPage


def get_page_for_url(url, playwright_page):
    if "emag.ro" in url:
        return EmagProductPage(playwright_page)
    raise ValueError(f"No page object configured for URL: {url}")

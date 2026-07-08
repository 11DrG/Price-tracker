from pages.base_page import BasePage
from pages.emag_page import EmagProductPage


def test_base_page_site_name_is_none():
    assert BasePage.site_name is None


def test_emag_page_site_name():
    assert EmagProductPage.site_name == "eMAG"


def test_emag_inherits_from_base_page():
    assert issubclass(EmagProductPage, BasePage)


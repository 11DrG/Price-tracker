from unittest.mock import MagicMock
from pages.emag_page import EmagProductPage


# --- eMAG ---

def _emag_page(html):
    p = EmagProductPage(MagicMock())
    p._html = html
    return p

def test_emag_get_current_price():
    html = 'data-test="main-price">279<sup><small class="mf-decimal">&#44;</small>98</sup>'
    assert _emag_page(html).get_current_price() == 279.98


def test_emag_get_original_price_returns_none_when_no_strikethrough():
    html = 'data-test="main-price">279<sup><small class="mf-decimal">&#44;</small>98</sup>'
    assert _emag_page(html).get_original_price(279.98) is None


def test_emag_get_original_price_returns_value_when_strikethrough_exists():
    html = '<s>350<sup><small class="mf-decimal">&#44;</small>00</sup> <span>Lei</span></s>'
    assert _emag_page(html).get_original_price(279.98) == 350.0


def test_emag_get_original_price_returns_none_when_original_lower_than_current():
    html = '<s>200<sup><small class="mf-decimal">&#44;</small>00</sup> <span>Lei</span></s>'
    assert _emag_page(html).get_original_price(279.98) is None


# (Altex and Carrefour tests removed — project now targets only eMAG)

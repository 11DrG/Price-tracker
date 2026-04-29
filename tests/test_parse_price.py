import pytest
from tracker import parse_price


def test_simple_price_with_comma_decimal():
    assert parse_price("120,99 Lei") == 120.99


def test_price_with_thousands_separator():
    assert parse_price("1.299,99 Lei") == 1299.99


def test_price_with_no_decimal():
    assert parse_price("120 Lei") == 120.0


def test_price_strips_currency_symbol():
    assert parse_price("99,00 RON") == 99.0


def test_price_with_extra_whitespace():
    assert parse_price("  85,50 Lei  ") == 85.5


def test_price_returns_float():
    result = parse_price("120,99 Lei")
    assert isinstance(result, float)

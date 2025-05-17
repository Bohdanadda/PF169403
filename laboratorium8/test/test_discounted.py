import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from calculate_discounted import calculate_discounted_price

@pytest.mark.parametrize("price, discount, expected", [
    (100, 10, 90.00),
    (200, 25, 150.00),
    (99.99, 5, 94.99),
    (0, 0, 0.00),
    (100, 0, 100.00),
    (100, 100, 0.00),
    (123.45, 33, 82.71)
])
def test_calculate_discounted_price_valid(price, discount, expected):
    assert calculate_discounted_price(price, discount) == expected


@pytest.mark.parametrize("price, discount", [
    (-100, 10),         #  ujemna
    ("100", 10),        # cena string
    (100, -10),         # rabat mniejszy
    (100, 150),         # rabat wyższy 100
    (100, "20"),        # rabat string
    (None, 10),         # brak ceny
    (100, None),        # brak rabatu
])
def test_calculate_discounted_price_invalid(price, discount):
    with pytest.raises(ValueError):
        calculate_discounted_price(price, discount)


def test_calculate_discounted_price_rounding():
    price = 100
    discount = 33.3333
    result = calculate_discounted_price(price, discount)
    assert result == 66.67
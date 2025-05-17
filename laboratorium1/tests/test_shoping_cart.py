import unittest

from laboratorium1.src.shopping_cart import ShoppingCart


class TestShopingCart(unittest.TestCase):

    def setUp(self):
        self.cart = ShoppingCart()

    def test_add_item(self):
        self.cart.add_item("Apple", 1.2, 5)
        self.assertIn("Apple", self.cart.items)
        self.assertEqual(self.cart.items["Apple"]["price"], 1.2)
        self.assertEqual(self.cart.items["Apple"]["quantity"], 5)

        self.cart.add_item("Orange", 1.5, 3)
        self.assertEqual(self.cart.items["Orange"], ["quantity"], )

    # def test_remove_item(self):
    #     self.

    def tearDown(self):
        pass
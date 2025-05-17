import unittest
from laboratorium1.src.is_palindrom import IsPalindrom

class TestIsPalindrom(unittest.TestCase):
    def setUp(self):
        self.is_palindrom = IsPalindrom()

    def test_palindrome_simple(self):
        self.assertTrue(self.is_palindrom.is_palindrom("kajak"))

    def test_palindrome_mixed_case(self):
        self.assertTrue(self.is_palindrom.is_palindrom("Madam"))

    def test_palindrome_with_punctuation(self):
        self.assertTrue(self.is_palindrom.is_palindrom("A man, a plan, a canal: Panama"))

    def test_not_palindrome(self):
        self.assertFalse(self.is_palindrom.is_palindrom("hello"))

    def test_empty_string(self):
        self.assertTrue(self.is_palindrom.is_palindrom(""))

    def test_single_character(self):
        self.assertTrue(self.is_palindrom.is_palindrom("x"))

    def tearDown(self):
        pass
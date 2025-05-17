import unittest
from laboratorium1.src.string_manipulator import StringManipulator


class TestStringManipulator(unittest.TestCase):
    def setUp(self):
        self.string_manipulator = StringManipulator()

    def test_revers_string(self):
        self.assertEqual(self.string_manipulator.revers_string("hello"), "olleh")
        self.assertEqual(self.string_manipulator.revers_string(""), "")
        self.assertEqual(self.string_manipulator.revers_string("Nice!"), "!eciN")
        self.assertEqual(self.string_manipulator.revers_string("12345"), "54321")

    def test_count_word(self):
        self.assertEqual(self.string_manipulator.count_words("Hello world"), 2)
        self.assertEqual(self.string_manipulator.count_words(""), 0)
        self.assertEqual(self.string_manipulator.count_words("XD!"), 1)
        self.assertEqual(self.string_manipulator.count_words("Ja dziś nie nie jadłem"), 5)

    def test_capitalize_words(self):
        self.assertEqual(self.string_manipulator.capitalize_words("hello world"), "Hello World")
        self.assertEqual(self.string_manipulator.capitalize_words("HELLO WORLD"), "Hello World")
        self.assertEqual(self.string_manipulator.capitalize_words("hello-world"), "Hello-World")
        self.assertEqual(self.string_manipulator.capitalize_words("hello_world 1263"), "Hello_World 1263")

    def tearDown(self):
        pass
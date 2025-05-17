import unittest
from laboratorium1.src.find_most_frequent_word import FindMostFrequentWord

class TestFindMostFrequentWord(unittest.TestCase):
    def setUp(self):
        self.find_most_frequent_word = FindMostFrequentWord()

    def test_empty_text(self):
        self.assertEqual(self.find_most_frequent_word.find_most_frequent_word(" "), None)

    def test_single_word(self):
        self.assertEqual(self.find_most_frequent_word.find_most_frequent_word("hello"), "hello")

    def test_multiple_words(self):
        self.assertEqual(self.find_most_frequent_word.find_most_frequent_word("apple banana apple"), "apple")

    def test_punctuation(self):
        self.assertEqual(self.find_most_frequent_word.find_most_frequent_word("Hello hello world, have a nice day, hello"), "hello")

    def tearDown(self):
        pass

if __name__ == "__main__":
    unittest.main()
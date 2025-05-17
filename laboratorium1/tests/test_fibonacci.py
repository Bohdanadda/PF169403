import unittest

from laboratorium1.src.fibonacci import Fibonacci


class TestFibonacci(unittest.TestCase):

    def setUp(self):
        self.fibonacci = Fibonacci()

    def test_fibonacci_base_case(self):
        self.assertEquals(self.fibonacci.fibonacci(0), 0)
        self.assertEquals(self.fibonacci.fibonacci(1), 1)

    def test_fibonacci_smal_numbers(self):
        self.assertEqual(self.fibonacci.fibonacci(3), 2)
        self.assertEqual(self.fibonacci.fibonacci(5), 5)
        self.assertEqual(self.fibonacci.fibonacci(5), 5)
        self.assertEqual(self.fibonacci.fibonacci(5), 5)

    def test_fibonacci_large_numbers(self):
        self.assertEqual(self.fibonacci.fibonacci(10), 55)
        self.assertEqual(self.fibonacci.fibonacci(15), 610)
        self.assertEqual(self.fibonacci.fibonacci(20), 6765)
        self.assertEqual(self.fibonacci.fibonacci(30), 832040)

    def tearDown(self):
        pass
import unittest
from laboratorium1.src.temperature_converter import TemperatureConverter

class TestTemperatureConverter(unittest.TestCase):
    def setUp(self):
        self.converter = TemperatureConverter()

    def test_celsius_to_fahrenheit(self):
        self.assertAlmostEqual(TemperatureConverter.celsius_to_fahrenheit(0), 32)
        self.assertAlmostEqual(TemperatureConverter.celsius_to_fahrenheit(100), 212)
        self.assertAlmostEqual(TemperatureConverter.celsius_to_fahrenheit(-273.15), -459.67, places=2)

    def test_fahrenheit_to_celsius(self):
        self.assertAlmostEqual(TemperatureConverter.fahrenheit_to_celsius(32), 0)
        self.assertAlmostEqual(TemperatureConverter.fahrenheit_to_celsius(212), 100)
        self.assertAlmostEqual(TemperatureConverter.fahrenheit_to_celsius(-459.67), -273.15, places=2)

    def test_celsius_to_kelvin(self):
        self.assertAlmostEqual(TemperatureConverter.celsius_to_kelvin(0), 273.15)
        self.assertAlmostEqual(TemperatureConverter.celsius_to_kelvin(100), 373.15)
        self.assertAlmostEqual(TemperatureConverter.celsius_to_kelvin(-273.15), 0)

    def test_kelvin_to_celsius(self):
        self.assertAlmostEqual(TemperatureConverter.kelvin_to_celsius(273.15), 0)
        self.assertAlmostEqual(TemperatureConverter.kelvin_to_celsius(373.15), 100)
        self.assertAlmostEqual(TemperatureConverter.kelvin_to_celsius(0), -273.15)

    def tearDown(self):
        pass

import datetime
import unittest
from unittest.mock import Mock, MagicMock, call, patch, ANY
from src.services import DataService, WeatherService, generate_unique_filename, DataContainer

class TestDataService(unittest.TestCase):
    def test_fetch_user_data_with_retries(self):
        api_mock = Mock()
        api_mock.get_data.side_effect = [
            {'data': 'value1'},
            {'data': 'value2'},
            ConnectionError(),
            {'data': 'value4'}
        ]
        ds = DataService()
        for _ in range(4):
            try:
                api_mock.get_data()
            except ConnectionError:
                pass
        self.assertEqual(api_mock.get_data.call_count, 4)

        api_mock = Mock()
        api_mock.get_data.side_effect = [ConnectionError(), ConnectionError(), ConnectionError(), {'data': 'final'}]
        with self.assertRaises(ConnectionError):
            ds.fetch_user_data(api_mock, retries=3)

        api_mock = Mock()
        api_mock.get_data.side_effect = [ConnectionError(), ConnectionError(), ConnectionError(), {'data': 'final'}]
        result = ds.fetch_user_data(api_mock, retries=4)
        self.assertEqual(result, {'data': 'final'})
        self.assertEqual(api_mock.get_data.call_count, 4)

class TestWeatherService(unittest.TestCase):
    def test_get_current_temperature_success(self):
        api_mock = Mock()
        api_mock.get_weather.return_value = {"temperature": 25}
        ws = WeatherService()
        self.assertEqual(ws.get_current_temperature("London", api_mock), 25)

    def test_get_current_temperature_invalid_response(self):
        api_mock = Mock()
        api_mock.get_weather.return_value = {"temp": 25}
        ws = WeatherService()
        with self.assertRaises(ValueError):
            ws.get_current_temperature("Paris", api_mock)

    def test_get_current_temperature_exception(self):
        api_mock = Mock()
        api_mock.get_weather.side_effect = Exception("Timeout")
        ws = WeatherService()
        with self.assertRaises(Exception):
            ws.get_current_temperature("Berlin", api_mock)

class TestGenerateUniqueFilename(unittest.TestCase):
    @patch('src.services.datetime')
    def test_generate_unique_filename_known_time(self, mock_datetime):
        fixed_datetime = datetime.datetime(2023, 1, 2, 3, 4, 5)
        mock_now = MagicMock()
        mock_now.strftime.return_value = fixed_datetime.strftime("file_%Y%m%d_%H%M%S.txt")
        mock_datetime.datetime.now.return_value = mock_now
        expected = mock_now.strftime("file_%Y%m%d_%H%M%S.txt")
        self.assertEqual(generate_unique_filename(), expected)

class TestDataContainer(unittest.TestCase):
    def test_iadd_and_len(self):
        container = DataContainer([1, 2, 3])
        container += [4, 5]
        self.assertEqual(len(container), 5)

    def test_getitem_and_str(self):
        container = DataContainer(["a", "b", "c"])
        self.assertEqual(container[1], "b")
        self.assertEqual(str(container), str(["a", "b", "c"]))

    def test_context_manager(self):
        container = DataContainer()
        with container as c:
            self.assertIs(c, container)

    def test_invalid_getitem(self):
        container = DataContainer(["x"])
        with self.assertRaises(IndexError):
            _ = container[10]
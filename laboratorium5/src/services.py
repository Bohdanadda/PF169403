import datetime

class DataService:
    def fetch_user_data(self, api, retries=3):
        attempt = 0
        while attempt < retries:
            try:
                return api.get_data()
            except ConnectionError:
                attempt += 1
                if attempt >= retries:
                    raise

class WeatherService:
    def get_current_temperature(self, city, api):
        try:
            response = api.get_weather(city)
            if not isinstance(response, dict) or "temperature" not in response:
                raise ValueError("Invalid API response")
            return response["temperature"]
        except Exception as e:
            raise

def generate_unique_filename():
    now = datetime.datetime.now()
    return now.strftime("file_%Y%m%d_%H%M%S.txt")

class DataContainer:
    def __init__(self, data=None):
        self._data = list(data) if data is not None else []

    def __iadd__(self, other):
        self._data += list(other)
        return self

    def __getitem__(self, key):
        return self._data[key]

    def __str__(self):
        return str(self._data)

    def __len__(self):
        return len(self._data)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
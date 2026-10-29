import unittest
from unittest.mock import Mock

import pandas as pd
import requests

from api_client import WeatherAPIClient, WeatherAPIError
from data_parser import WeatherDataParser, WeatherParseError

SAMPLE_PAYLOAD = {
    "hourly": {
        "time": ["2026-10-29T00:00", "2026-10-29T01:00", "2026-10-29T02:00"],
        "temperature_2m": [24.1, 23.8, None],
        "wind_speed_10m": [12.4, 10.0, 9.5],
    }
}


class TestWeatherAPIClient(unittest.TestCase):
    def make_client(self, response=None, error=None):
        session = Mock()
        if error:
            session.get.side_effect = error
        else:
            session.get.return_value = response
        return WeatherAPIClient(session=session), session

    def test_get_forecast_success(self):
        response = Mock()
        response.json.return_value = SAMPLE_PAYLOAD
        client, session = self.make_client(response=response)

        result = client.get_forecast(25.0, 51.0)

        self.assertEqual(result, SAMPLE_PAYLOAD)
        _, kwargs = session.get.call_args
        self.assertEqual(kwargs["params"]["latitude"], 25.0)
        self.assertEqual(kwargs["params"]["longitude"], 51.0)
        self.assertEqual(kwargs["timeout"], 10)

    def test_http_error_is_wrapped(self):
        response = Mock()
        response.raise_for_status.side_effect = requests.HTTPError("500")
        client, _ = self.make_client(response=response)

        with self.assertRaises(WeatherAPIError):
            client.get_forecast(25.0, 51.0)

    def test_timeout_is_wrapped(self):
        client, _ = self.make_client(error=requests.Timeout("too slow"))

        with self.assertRaises(WeatherAPIError):
            client.get_forecast(25.0, 51.0)

    def test_invalid_json_is_wrapped(self):
        response = Mock()
        response.json.side_effect = ValueError("bad json")
        client, _ = self.make_client(response=response)

        with self.assertRaises(WeatherAPIError):
            client.get_forecast(25.0, 51.0)


class TestWeatherDataParser(unittest.TestCase):
    def setUp(self):
        self.parser = WeatherDataParser()

    def test_valid_payload_returns_dataframe(self):
        df = self.parser.parse(SAMPLE_PAYLOAD)

        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(df.shape, (3, 2))
        self.assertIsInstance(df.index, pd.DatetimeIndex)
        self.assertEqual(df["wind_speed_10m"].iloc[0], 12.4)

    def test_null_becomes_nan(self):
        df = self.parser.parse(SAMPLE_PAYLOAD)

        self.assertTrue(pd.isna(df["temperature_2m"].iloc[2]))

    def test_non_dict_payload_raises(self):
        with self.assertRaises(WeatherParseError):
            self.parser.parse([1, 2, 3])

    def test_missing_hourly_raises(self):
        with self.assertRaises(WeatherParseError):
            self.parser.parse({"daily": {}})

    def test_missing_time_raises(self):
        with self.assertRaises(WeatherParseError):
            self.parser.parse({"hourly": {"temperature_2m": [1, 2]}})

    def test_mismatched_lengths_raise(self):
        payload = {"hourly": {"time": ["2026-10-29T00:00"], "temperature_2m": [1, 2]}}

        with self.assertRaises(WeatherParseError):
            self.parser.parse(payload)

    def test_empty_hourly_returns_empty_dataframe(self):
        df = self.parser.parse({"hourly": {"time": []}})

        self.assertTrue(df.empty)


if __name__ == "__main__":
    unittest.main()

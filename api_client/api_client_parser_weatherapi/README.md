# Weather API Project

Fetches hourly weather data from the free [Open-Meteo](https://open-meteo.com/)
REST API (HTTP GET), parses the JSON into a pandas DataFrame, and includes unit
tests using `unittest` and mock objects.

## Project structure

| File | Purpose |
|---|---|
| `api_client.py` | `WeatherAPIClient` - sends the HTTP GET request |
| `data_parser.py` | `WeatherDataParser` - converts JSON to a pandas DataFrame |
| `main.py` | Ties the client and parser together and prints the result |
| `test_project.py` | Unit tests (mocked) |
| `requirements.txt` | Dependencies: `requests`, `pandas` |

## How to run

```
pip install -r requirements.txt
python main.py                          
python main.py --lat 25.2 --lon 55.3    
python -m unittest -v                   # run the tests
```

## Output

`python main.py` prints the number of rows and columns, the first 10 rows of the
DataFrame, and a statistical summary (`describe()`). By default it requests 3
days of hourly data (72 rows, 5 columns). If a request or parse step fails, it
prints `Error: ...` and exits with code 1 instead of showing a traceback.

## Example: received JSON and parsed DataFrame

> The data below is **sample data** in Open-Meteo's response format, used to
> illustrate the parsing. Real values will differ.

**Received JSON (shortened to 4 hours):**

```json
{
  "latitude": 25.2854,
  "longitude": 51.531,
  "timezone": "Asia/Qatar",
  "hourly_units": {
    "time": "iso8601", "temperature_2m": "°C", "wind_speed_10m": "km/h",
    "wind_gusts_10m": "km/h", "precipitation": "mm", "visibility": "m"
  },
  "hourly": {
    "time": ["2026-10-29T00:00", "2026-10-29T01:00", "2026-10-29T02:00", "2026-10-29T03:00"],
    "temperature_2m": [28.4, 28.1, 27.7, null],
    "wind_speed_10m": [14.2, 13.8, 12.5, 11.9],
    "wind_gusts_10m": [26.3, 25.1, 23.8, 22.0],
    "precipitation": [0.0, 0.0, 0.0, 0.0],
    "visibility": [24140.0, 24140.0, 22000.0, 20500.0]
  }
}
```

**Parsed pandas DataFrame:**

```
                     temperature_2m  wind_speed_10m  wind_gusts_10m  precipitation  visibility
time
2026-10-29 00:00:00            28.4            14.2            26.3            0.0     24140.0
2026-10-29 01:00:00            28.1            13.8            25.1            0.0     24140.0
2026-10-29 02:00:00            27.7            12.5            23.8            0.0     22000.0
2026-10-29 03:00:00             NaN            11.9            22.0            0.0     20500.0
```

All columns are `float64` and `time` is a `DatetimeIndex`. The JSON `null`
becomes `NaN`.

## Error handling

Handles HTTP errors and invalid or missing data, with a custom exception per layer:

- **`api_client.py` - `WeatherAPIError`**
  - `raise_for_status()` turns 4xx/5xx responses into an `HTTPError`.
  - `except requests.RequestException` catches timeouts, connection/DNS failures and HTTP errors.
  - `except ValueError` catches responses that are not valid JSON.
  - All are re-raised as `WeatherAPIError` (with `from exc`, so the original cause is kept).
- **`data_parser.py` - `WeatherParseError`**
  - Checks the payload is a dictionary.
  - Checks the `hourly` section and its `time` list exist.
  - Checks every column has the same length as `time`.
  - `pd.to_numeric(errors="coerce")` turns bad or null values into `NaN` instead of crashing.
- **`main.py`** catches both custom exceptions, prints a clean message and exits with code 1.

Example parser errors:

```
not a dict:      WeatherParseError -> Payload must be a dictionary
no hourly:       WeatherParseError -> Payload is missing 'hourly' data with 'time'
length mismatch: WeatherParseError -> 'temperature_2m' has 2 values, expected 1
```

## Unit testing

Tests the API client and the data parsing using `unittest` and mock objects
(`unittest.mock`). 11 tests, none of which use the internet.

- **Client tests (4):** a `Mock()` replaces the `requests` session so the test
  controls what the "server" returns. They check the correct params and timeout
  are sent on success, and that an HTTP error, a timeout and invalid JSON each
  become a `WeatherAPIError`.
- **Parser tests (7):** use a fixed sample payload and check the DataFrame type,
  shape, datetime index and values; that a null becomes `NaN`; that a non-dict
  payload, missing `hourly`, missing `time` and mismatched lengths raise
  `WeatherParseError`; and that an empty `hourly` returns an empty DataFrame.

Mocking makes the tests fast and repeatable, and lets them simulate failures that
are hard to trigger on a real API.

## Data source

Weather data by [Open-Meteo.com](https://open-meteo.com/), licensed under
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). The free API needs no
key and is for non-commercial use. 




**NidhinDaniel**

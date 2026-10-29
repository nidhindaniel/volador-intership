import requests
class WeatherAPIError(Exception):
    """Raised when the weather API request fails."""
class WeatherAPIClient:
    BASE_URL = "https://api.open-meteo.com/v1/forecast"
    DEFAULT_HOURLY = (
        "temperature_2m",
        "wind_speed_10m",
        "wind_gusts_10m",
        "precipitation",
        "visibility",
    )

    def __init__(self, timeout=10, session=None):
        self.timeout = timeout
        self.session = session or requests.Session()

    def get_forecast(self, latitude, longitude, hourly=None, forecast_days=3):
        """Send a GET request and return the decoded JSON as a dict."""
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "hourly": ",".join(hourly or self.DEFAULT_HOURLY),
            "forecast_days": forecast_days,
            "timezone": "auto",
        }

        try:
            response = self.session.get(
                self.BASE_URL, params=params, timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as exc:
            raise WeatherAPIError(f"Weather API request failed: {exc}") from exc
        except ValueError as exc:  
            raise WeatherAPIError("Weather API returned invalid JSON") from exc

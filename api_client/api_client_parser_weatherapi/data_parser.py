import pandas as pd
class WeatherParseError(ValueError):
    """Raised when the API response does not have the expected structure."""
class WeatherDataParser:
    def parse(self, payload):
        """Convert the 'hourly' section of the response into a DataFrame.

        The API returns parallel lists (one list per variable). Each list
        becomes a column, and 'time' becomes a datetime index.
        """
        if not isinstance(payload, dict):
            raise WeatherParseError("Payload must be a dictionary")

        hourly = payload.get("hourly")
        if not isinstance(hourly, dict) or "time" not in hourly:
            raise WeatherParseError("Payload is missing 'hourly' data with 'time'")

        length = len(hourly["time"])
        for name, values in hourly.items():
            if not isinstance(values, list):
                raise WeatherParseError(f"'{name}' must be a list")
            if len(values) != length:
                raise WeatherParseError(
                    f"'{name}' has {len(values)} values, expected {length}"
                )

        df = pd.DataFrame(hourly)
        df["time"] = pd.to_datetime(df["time"])
        df = df.set_index("time")
        for column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce")

        return df

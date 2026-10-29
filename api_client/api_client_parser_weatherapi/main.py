import argparse
import pandas as pd
from api_client import WeatherAPIClient, WeatherAPIError
from data_parser import WeatherDataParser, WeatherParseError


def main():
    pd.set_option("display.width", 200)
    pd.set_option("display.max_columns", None)

    arg_parser = argparse.ArgumentParser(description="Fetch and parse weather data")
    arg_parser.add_argument("--lat", type=float, default=25.2854, help="latitude")
    arg_parser.add_argument("--lon", type=float, default=51.5310, help="longitude")
    args = arg_parser.parse_args()

    client = WeatherAPIClient()
    parser = WeatherDataParser()

    try:
        payload = client.get_forecast(args.lat, args.lon)
        df = parser.parse(payload)
    except (WeatherAPIError, WeatherParseError) as exc:
        print(f"Error: {exc}")
        return 1

    print(f"Rows: {len(df)}  |  Columns: {list(df.columns)}\n")
    print(df.head(10))
    print("\nSummary:")
    print(df.describe().round(2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

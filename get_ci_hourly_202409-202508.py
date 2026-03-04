import pandas as pd
import pytz
import requests
from tqdm import tqdm

from datetime import timedelta

Date_format_api = "%Y-%m-%dT%H:%MZ"
time_window = timedelta(hours=1)

date_range = pd.date_range(start="2024-09-01", end="2025-08-31", freq="H", tz=pytz.UTC)

tqdm.pandas()

def get_ci(date):
    from_utc = date
    to_utc = from_utc + time_window
    from_string = from_utc.strftime(Date_format_api)
    to_string = to_utc.strftime(Date_format_api)

    # Querying the API (request) for each job
    url = f"https://api.carbonintensity.org.uk/intensity/{from_string}/{to_string}"
    try: 
        # Make the GET request to the API 
        api_response = requests.get(url, headers={"Accept": "application/json"}, timeout=10)

        # raise an error if the request was unsuccessful
        api_response.raise_for_status()

        # Parse the JSON response as JSON format 
        json_CI_response = api_response.json()

        # Extract the carbon intensity value (gCO2e/kWh) from the response
        carbon_intensity = json_CI_response["data"][0]["intensity"]["actual"]

        print(f"{from_string}, {carbon_intensity}")

    except Exception as e:
        print(f"Error querying API for time {from_string} to {to_string}: {e}")
        carbon_intensity = None

    return carbon_intensity


df = pd.DataFrame(date_range, columns=["datetime_utc"])
df["carbon_intensity_gCO2e_per_kWh"] = df["datetime_utc"].progress_apply(get_ci)

df.to_csv("./data/ci_hourly_202409-202508.csv", index=False)
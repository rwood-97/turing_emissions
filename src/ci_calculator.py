import pandas as pd
import pytz
import requests

from datetime import timedelta

## Adapted from GRACE-HPC
## https://github.com/Elliot-Ayliffe/GRACE-HPC

class CarbonIntensityCalculator():
    def __init__(self):
        self.cached_value = {}

    # Function for querying the Carbon Intensity API for realtime carbon intensity data
    def get_carbon_intensity(self, submission_times):
        """
        For each job submission time, this function queries the Carbon Intensity API for the specified region
        and returns the carbon intensity value (gCO2e/kWh) for that time. If the API fails, it falls back
        to the UK average carbon intensity value (2024).

        API documentation: https://carbon-intensity.github.io/api-definitions/#get-regional-intensity-from-to-regionid-regionid

        Args:
            submission_times (pd.Series): Series of datetime job submission timestamps ('SubmissionTime' column)

        Return:
            pd.Series: Series of carbon intensity values (gCO2e/kWh) corresponding to each job.
        """
        # Define constants for the API
        Date_format_api = "%Y-%m-%dT%H:%MZ"
        
        time_window = timedelta(days=1)   # 1 day time window for aggregated carbon intensity values
        
        default_CI = 124       # Average UK carbon intensity of electricity (gCO2e/kWh) - 2024 - https://www.carbonbrief.org/analysis-uks-electricity-was-cleanest-ever-in-2024/ 

        # Set the region for which to get carbon intensity data.
        # region_name = "West Midlands"
        region_id = 8

        # Loop over each job submission time and query the API 
        carbon_intensity_values = []
        for submission_time in submission_times:
            try:
                # Confirm that the datetime is in UTC and timezone-aware for API compatibility 
                if submission_time.tzinfo is None:
                    # from_utc = DateTime.tz_localize("Europe/London").tz_convert("UTC")
                    from_utc = submission_time.replace(tzinfo=pytz.UTC)
                else:
                    # from_utc = DateTime.tz_convert("UTC")
                    from_utc = submission_time.astimezone(pytz.UTC)
            except Exception as e:
                print(f"Error converting datetime {submission_time} to UTC: {e}")
                carbon_intensity_values.append(default_CI)
                continue
            
            # Drop hours, minutes and seconds
            from_utc = from_utc.replace(hour=0, minute=0, second=0)
            if from_utc in self.cached_value:
                carbon_intensity_values.append(self.cached_value[from_utc])
                continue

            to_utc = from_utc + time_window         # the end time is the start time + time window
            from_string = from_utc.strftime(Date_format_api)
            to_string = to_utc.strftime(Date_format_api)

            # Querying the API (request) for each job
            url = f"https://api.carbonintensity.org.uk/regional/intensity/{from_string}/{to_string}/regionid/{region_id}"
            try: 
                # Make the GET request to the API 
                api_response = requests.get(url, headers={"Accept": "application/json"}, timeout=10)

                # raise an error if the request was unsuccessful
                api_response.raise_for_status()

                # Parse the JSON response as JSON format 
                json_CI_response = api_response.json()

                # Extract the carbon intensity value (gCO2e/kWh) from the response
                # Average over all 30-min slots in the 24-hour window
                slots = json_CI_response["data"]["data"]
                carbon_intensity = sum(s["intensity"]["forecast"] for s in slots) / len(slots)

                # Append the value to the list
                carbon_intensity_values.append(carbon_intensity)
                self.cached_value[from_utc] =  carbon_intensity # Cache the value

            except Exception as e:
                # If the API request fails, use the default carbon intensity value (UK annual average)
                print(f"Failed to get carbon intensity for {submission_time} from the API. Using UK average: {default_CI} gCO2e/kWh. Error: {e}")
                carbon_intensity_values.append(default_CI)

        # Return the carbon intensity values as a pandas Series with the same index as submission_times
        return pd.Series(carbon_intensity_values, index=submission_times.index)
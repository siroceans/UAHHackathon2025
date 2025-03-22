import requests
import json
import csv
import time

### Querry a specific time stamp
DATASTREAM_ID = "mlme3gtdfepvc"
STANDARD = "swe"
#STANDARD = "om"
FORMAT = "csv"
#FORMAT = "json"
TIME = "latest"
PARAM = "time"
# Time Stamp Request: Format: JSON ; STANDARD = SWE ; TIME = Latest
API_request = f"https://api.georobotix.io/ogc/t18/api/datastreams/{DATASTREAM_ID}/observations?f=application%2F{STANDARD}%2B{FORMAT}&{PARAM}={TIME}"
# API_request = f"https://api.georobotix.io/ogc/t18/api/datastreams/{DATASTREAM_ID}/observations?f=application%2F{STANDARD}%2B{FORMAT}"
# raw = requests.get(API_request,params={'time': 'latest'}) # alternate way to request time stamp
raw = requests.get(API_request)

print()
print("API Request URL:")
print(API_request)
print()
print("Latest API Response:")
print(raw.text) # Print
print()
print("raw data type:")
print(type(raw)) # Print

file_path = 'latest_pred_data_file.csv'

# Save API response as CSV
with open(file_path, "w", newline="") as file:
    file.write(raw.text)

print(f"\nResponse saved to {file_path}")

# ### Update Orientation Every 5 Minutes
# while True:
#     # Code to be executed every 5 minutes
#     print("Executing code...")
#     # Replace this with your actual code
#     time.sleep(300)  # 5 minutes * 60 seconds

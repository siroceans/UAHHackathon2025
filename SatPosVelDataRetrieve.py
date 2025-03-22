import requests
import json
import csv
import time

def getSatPos():
    ### Querry a specific time stamp
    DATASTREAM_ID = "ceuaig4rlf746"
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

    # print()
    # print("API Request URL:")
    # print(API_request)
    # print()
    # print("Latest API Response:")
    # print(raw.text) # Print
    # print()
    # print("raw data type:")
    # print(type(raw)) # Print

    file_path = 'latest_SPOT6_data_file.csv'

    # Save API response as CSV
    with open(file_path, "w", newline="") as csv_file:
        csv_file.write(raw.text)

    #print(f"\nResponse saved to {csv_file}")


    with open(file_path, "r") as csv_file:
        reader = csv.reader(csv_file)
        last_data = None
        for row in reader:  # Iterate to the last row
            last_data = row
        # if last_data:
        #     print("\nLast row in CSV file:", last_data)
        # else:
        #     print("\nCSV file is empty.")

    current_time = last_data[0]
    current_pos = [float(last_data[1]), float(last_data[2]), float(last_data[3])]

    #print(current_orientation)
    return(current_pos)
    # ### Update Orientation Every 5 Minutes
    # while True:
    #     # Code to be executed every 5 minutes
    #     print("Executing code...")
    #     # Replace this with your actual code
    #     time.sleep(300)  # 5 minutes * 60 seconds
def getSatVel():
    ### Querry a specific time stamp
    DATASTREAM_ID = "nrq0hf0h1mofa"
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

    # print()
    # print("API Request URL:")
    # print(API_request)
    # print()
    # print("Latest API Response:")
    # print(raw.text) # Print
    # print()
    # print("raw data type:")
    # print(type(raw)) # Print

    file_path = 'latest_SPOT6_data_file.csv'

    # Save API response as CSV
    with open(file_path, "w", newline="") as csv_file:
        csv_file.write(raw.text)

    #print(f"\nResponse saved to {csv_file}")


    with open(file_path, "r") as csv_file:
        reader = csv.reader(csv_file)
        last_data = None
        for row in reader:  # Iterate to the last row
            last_data = row
        # if last_data:
        #     print("\nLast row in CSV file:", last_data)
        # else:
        #     print("\nCSV file is empty.")

    current_time = last_data[0]
    current_vel = [float(last_data[1]), float(last_data[2]), float(last_data[3])]

    #print(current_orientation)
    return(current_vel)
    # ### Update Orientation Every 5 Minutes
    # while True:
    #     # Code to be executed every 5 minutes
    #     print("Executing code...")
    #     # Replace this with your actual code
    #     time.sleep(300)  # 5 minutes * 60 seconds
print(getSatPos())
print(getSatVel())
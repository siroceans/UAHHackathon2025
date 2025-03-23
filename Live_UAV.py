import numpy as np
import requests
import csv
import pyvista as pv
import imageio.v2 as imageio
import time
from scipy.spatial.transform import Rotation as R, Slerp


def getYawPitchRoll():
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

    # print()
    # print("API Request URL:")
    # print(API_request)
    # print()
    # print("Latest API Response:")
    # print(raw.text) # Print
    # print()
    # print("raw data type:")
    # print(type(raw)) # Print

    file_path = 'latest_pred_data_file.csv'

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
    current_orientation = [float(last_data[1]), float(last_data[2]), float(last_data[3])]

    #print(current_orientation)
    return(current_orientation)
    # ### Update Orientation Every 5 Minutes
    # while True:
    #     # Code to be executed every 5 minutes
    #     print("Executing code...")
    #     # Replace this with your actual code
    #     time.sleep(300)  # 5 minutes * 60 seconds
data = getYawPitchRoll()
print(data[0])
print(data[1])
print(data[2])
print(getYawPitchRoll())



def ten_thousand():
    yaw_array = []
    pitch_array = []
    roll_array = []

    for ii in range(0,500):
        new_data = getYawPitchRoll()
        yaw = new_data[0]
        pitch = new_data[1]
        roll = new_data[2]
        yaw_array.append(yaw)
        pitch_array.append(pitch)
        roll_array.append(roll)
        time.sleep(0.15)

    return yaw_array, pitch_array, roll_array

def UAV_mapper(yaw_array, pitch_array, roll_array, file_name):

    #load in the model
    mesh = pv.read(file_name)
    plotter = pv.Plotter(off_screen=True)
    pic_frame = []

    for ii,jj,kk in zip(np.array(yaw_array), np.array(pitch_array), np.array(roll_array)):
        trans_mesh = mesh.copy()
    #Rotation operation on the UAV
        trans_mesh.rotate_x(kk, inplace=True)
        trans_mesh.rotate_y(jj, inplace=True)
        trans_mesh.rotate_z(ii, inplace=True)

    #Plotting!!
        plotter.clear()
        plotter.add_mesh(trans_mesh, color='FF8FED', show_edges= True)
        plotter.show(auto_close=False)


    #Gather Frames
        frame = plotter.screenshot(return_img = True)
        pic_frame.append(frame)

    #Generate GIF
    imageio.mimsave("Live_UAV_Rotation.gif", pic_frame, duration=2, loop = 0)  # Adjust speed with duration
    print("GIF saved as Live_UAV_Rotation.gif!")
    return None

def maresmooth(a1, a2):
    steps = 100
    t = np.linspace(0, 1, steps)
    t2 = (1 - np.cos(t * np.pi)) / 2
    smoothing = a1 + (a2 - a1) * t2
    return smoothing

data = ten_thousand()
yaw_array = data[0]
pitch_array = data[1]
roll_array = data[2]
tol = 2
for i in range(len(yaw_array)):
    if i != 0: 
        diffyaw = yaw_array[i] - yaw_array[i-1]
        diffpitch = pitch_array[i] - pitch_array[i-1]
        diffroll = roll_array[i] - pitch_array[i-1]
        
        if abs(diffyaw) > tol:
            smoothing = maresmooth(yaw_array[i-1], yaw_array[i])
            hold = np.ones(len(smoothing))
            yaw_array = np.insert(yaw_array, i, smoothing)
            pitch_array = np.insert(pitch_array, i, hold * pitch_array[i])
            roll_array = np.insert(roll_array, i, hold * roll_array[i])


UAV_mapper(yaw_array, pitch_array, roll_array, 'Untitled.stl')


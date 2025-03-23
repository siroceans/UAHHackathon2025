import numpy as np
import requests
import csv
import pyvista as pv
import imageio.v2 as imageio
import time


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

def UAV_mapper(yaw_array, pitch_array, roll_array, file_name, texture_file):

    #load in the model
    mesh = pv.read(file_name)
    textures = pv.read_texture(texture_file)
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
        plotter.add_mesh(trans_mesh, color='FF8FED', show_edges= True, texture=textures )
        plotter.show(auto_close=False)


    #Gather Frames
        frame = plotter.screenshot(return_img = True)
        pic_frame.append(frame)

    #Generate GIF
    imageio.mimsave("Live_UAV_Rotation.gif", pic_frame, duration=2, loop = 0)  # Adjust speed with duration
    print("GIF saved as Live_UAV_Rotation.gif!")
    return None

data = ten_thousand()
yaw_array = data[0]
print(yaw_array)
print(len(yaw_array))
pitch_array = data[1]
print(pitch_array)
roll_array = data[2]
print(roll_array)

UAV_mapper(yaw_array, pitch_array, roll_array, 'CUPIC_JEt.obj', 'JETSurface_Color.png')



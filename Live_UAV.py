import numpy as np
import requests
import csv
import pyvista as pv
import imageio.v2 as imageio
import time
from scipy.spatial.transform import Rotation as R, Slerp


def getYawPitchRoll():
    DATASTREAM_ID = "mlme3gtdfepvc"
    STANDARD = "swe"
    FORMAT = "csv"
    TIME = "latest"
    PARAM = "time"
    API_request = f"https://api.georobotix.io/ogc/t18/api/datastreams/{DATASTREAM_ID}/observations?f=application%2F{STANDARD}%2B{FORMAT}&{PARAM}={TIME}"

    raw = requests.get(API_request)
    file_path = 'latest_pred_data_file.csv'

    with open(file_path, "w", newline="") as csv_file:
        csv_file.write(raw.text)

    with open(file_path, "r") as csv_file:
        reader = csv.reader(csv_file)
        last_data = None
        for row in reader:
            last_data = row

    if not last_data or len(last_data) < 4:
        print("❌ CSV row too short or malformed:")
        print(last_data)
        raise IndexError("Expected at least 4 columns in data row but got: " + str(len(last_data)))

    current_orientation = [float(last_data[1]), float(last_data[2]), float(last_data[3])]
    return current_orientation


def ten_thousand():
    yaw_array = []
    pitch_array = []
    roll_array = []

    for ii in range(0, 10000):
        orientation = getYawPitchRoll()
        yaw_array.append(orientation[0])
        pitch_array.append(orientation[1])
        roll_array.append(orientation[2])
        time.sleep(0.15)

    return yaw_array, pitch_array, roll_array


def maresmooth(a1, a2):
    steps = 100
    t = np.linspace(0, 1, steps)
    t2 = (1 - np.cos(t * np.pi)) / 2
    smoothing = a1 + (a2 - a1) * t2
    return smoothing


def UAV_mapper(yaw_array, pitch_array, roll_array, file_name):
    mesh = pv.read(file_name)
    plotter = pv.Plotter(off_screen=True)
    pic_frame = []

    for ii, jj, kk in zip(yaw_array, pitch_array, roll_array):
        trans_mesh = mesh.copy()
        trans_mesh.rotate_x(kk, inplace=True)
        trans_mesh.rotate_y(jj, inplace=True)
        trans_mesh.rotate_z(ii, inplace=True)

        plotter.clear()
        plotter.set_background("#000000")
        plotter.add_mesh(trans_mesh, color='3C4047', show_edges=True, edge_color="white", line_width=1.5)

        # Format Euler angles for display
        angle_text = f"Yaw: {ii:.2f}°, Pitch: {jj:.2f}°, Roll: {kk:.2f}°"
        plotter.add_text(angle_text, position="lower_edge", font_size=12, color="white")

        plotter.show(auto_close=False)
        frame = plotter.screenshot(return_img=True)
        pic_frame.append(frame)

    imageio.mimsave("Live_UAV_Rotation.gif", pic_frame, duration=2, loop=0)
    print("✅ GIF saved as Live_UAV_Rotation.gif!")


# Run the data collection
yaw_array, pitch_array, roll_array = ten_thousand()

# Apply smoothing if needed
tol = 2
for i in range(len(yaw_array)):
    if i != 0:
        diffyaw = yaw_array[i] - yaw_array[i - 1]
        diffpitch = pitch_array[i] - pitch_array[i - 1]
        diffroll = roll_array[i] - roll_array[i - 1]

        if abs(diffyaw) > tol:
            smoothing = maresmooth(yaw_array[i - 1], yaw_array[i])
            hold = np.ones(len(smoothing))
            yaw_array = np.insert(yaw_array, i, smoothing)
            pitch_array = np.insert(pitch_array, i, hold * pitch_array[i])
            roll_array = np.insert(roll_array, i, hold * roll_array[i])

# Generate the GIF with Euler angles
UAV_mapper(yaw_array, pitch_array, roll_array, 'Untitled.stl')

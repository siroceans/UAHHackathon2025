import pyvista as pv
import imageio.v2 as imageio
import numpy as np
import pandas as pd
from UAVOrientationDataRetrieve import getYawPitchRoll
def UAV_mapper():
#load in data
    data = pd.read_csv('PlanformAttitude.csv')

    time = np.array(data.iloc[:,0])
    yaw = np.array(data.iloc[:,1])
    pitch = np.array(data.iloc[:,2])
    roll = np.array(data.iloc[:,3])
    plotter = pv.Plotter(off_screen=True)


    #load in the model
    mesh = pv.read('Untitled.stl')

    pic_frame = []

    for ii,jj,kk in zip(yaw, pitch, roll):
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
    imageio.mimsave("UAV_Rotation.gif", pic_frame, duration=0.00001, loop = 0)  # Adjust speed with duration
    print("GIF saved as UAV_Rotation.gif!")
    return None
UAV_mapper()

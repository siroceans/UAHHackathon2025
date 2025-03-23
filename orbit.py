import numpy as np
from math import factorial, sin, sqrt, cos, sinh, cosh 
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import trimesh
import pyvista as pv
import imageio
import SatPosVelDataRetrieve as data

def mag(v):
    magnitude = np.sqrt(np.sum(v**2))
    return magnitude

def futurePosition(r, v, dt):
    """
    Function that solves the TOF Equation iteratively to calculate the position 
    at a given time after the observation!

    """
    # Calculations of orbital parameters
    maxno = 100
    tol = 0.001 # Tolerance for iterative solutions
    mu = 3.986004418 * 10 ** 5
    #mu = 1
    r = np.array(r)
    v = np.array(v)
    rmag = mag(r)
    vmag = mag(v)
    h = np.cross(r,v)
    hmag = mag(h)
    e = (1/mu) * ((vmag**2 - mu/rmag) * r - np.dot(r,v) * v)
    emag = mag(e) 
    a = hmag ** 2 / (mu * (1 - emag ** 2))
    n = np.sqrt(1/a**3)
    
    # Iterative Process
    xn = np.sqrt(mu) * dt / a 
    i = 0
    check = True
    
    while check:
        i += 1
        # Not printing iteration tables as of right now!
        
        z = xn**2/a
        if abs(z) < tol:
            s = 1 / factorial(3) - z / factorial(5) + z**2 / factorial(7) - z**3 / factorial(9)
            c = 1 / factorial(2) - z / factorial(4) + z**2 / factorial(6) - z**3 / factorial(8)
        elif z > 0:
            s = (sqrt(z) - sin(sqrt(z))) / sqrt(z**3); 
            c = (1 - cos(sqrt(z))) / z; 
        else:
            s = (sinh(sqrt(-z)) - sqrt(-z)) / sqrt((-z)**3)
            c = (1 - cosh(sqrt(-z)))/z
        
        t = (1 / sqrt(mu)) * (xn**3 * s + np.dot(r,v) / sqrt(mu) * xn**2 * c + rmag * xn * (1-z*s))
        rn = xn**2 * c + np.dot(r,v) / sqrt(mu) * xn * (1-z*s) + rmag*(1 - z * c)
        dtdx = rn / sqrt(mu)
        xn1 = xn + (dt - t) / (dtdx)
        
        if abs(dt-t) < tol or i > maxno:
            break
        else:
            xn = xn1
        
    f = 1 - xn ** 2 / rmag * c 
    g = t - xn ** 3 / sqrt(mu) * s
    fdot = (sqrt(mu) * xn) / (rmag * rn) * (z * s - 1) 
    gdot = 1 - xn ** 2 / rn * c 
    
    r2 = f * r + g * v 
    v2 = fdot * r + gdot * v 
    
    r2 = np.array(r2).tolist()
    v2 = np.array(v2).tolist()
#    print("r2 = [{:.4f}, {:.4f}, {:.4f}]".format(r2[0], r2[1], r2[2]))
#    print("v2 = [{:.4f}, {:.4f}, {:.4f}]".format(v2[0], v2[1], v2[2]))
    return r2, v2    
    
def orbitPlotting(r, v):
    mu = 3.986004418 * 10 ** 5
    r = np.array(r)
    v = np.array(v)
    rmag = mag(r)
    vmag = mag(v)
    h = np.cross(r,v)
    hmag = mag(h)
    e = (1/mu) * ((vmag**2 - mu/rmag) * r - np.dot(r,v) * v)
    emag = mag(e) 
    a = hmag ** 2 / (mu * (1 - emag ** 2))
    n = np.cross(np.array([0,0,1]),h)
    n[2] = 0
    nmag = mag(n)
    i = np.arccos(h[2]/hmag)
    omega = np.arccos(n[0]/nmag)
    w = np.arccos(np.dot(n, e)/(nmag*emag))
    
    if n[1] < 0:
        omega = 2*np.pi - omega
    if e[2] < 0:
        w = 2*np.pi - w
        
    # Transformation matrix to rotate the elliptic orbit
    R11 = cos(omega) * cos(w) - sin(omega) * sin(w) * cos(i)
    R12 = -cos(omega) * sin(w) - sin(omega) * cos(omega) * cos(i)
    R13 = sin(omega) * sin(i)
    R21 = sin(omega) * cos(omega) + cos(omega) * sin(w) * cos(i)
    R22 = -sin(omega) * sin(w) + cos(omega) * cos(w) * cos(i)
    R23 = -cos(omega) * sin(i)
    R31 = sin(w) * sin(i)
    R32 = cos(w) * sin(i)
    R33 = cos(i)
    
    R = np.array([[R11, R12, R13], [R21, R22, R23], [R31, R32, R33]])
    
    # Orbital components for plotting!
    theta = np.linspace(0, 2*np.pi, num = 500)
    x = np.zeros_like(theta)
    y = np.zeros_like(theta)
    z = np.zeros_like(theta)
    
    for angle in range(len(theta)):
        ra = a * (1-emag ** 2) / (1 + emag * cos(theta[angle]))
        x[angle] = ra * cos(theta[angle])
        y[angle] = ra * sin(theta[angle])
        
    coordinates_perifocal = np.transpose(np.column_stack((x, y, z)))
    coordinates = np.matmul(R, coordinates_perifocal)
    
    x = np.transpose(coordinates[0,:])
    y = np.transpose(coordinates[1,:])
    z = np.transpose(coordinates[2,:])
    
    # Doing all of the plotting!
    scale = 5
    scale2 = 15   
    earth = pv.read("objectFiles/earth.obj")
    earth_texture = pv.read_texture("objectFiles/earth.jpg")
    earth = earth.scale([scale, scale, scale])
    satellite = pv.read("objectFiles/satellite.obj")
    satellite = satellite.scale([scale2, scale2, scale2])
    satellite_texture = pv.read_texture("objectFiles/satellite.png")
    satellite = satellite.translate([r[0], r[1], r[2]])
    
    plotter = pv.Plotter()
    plotter.background_color = "#000000"
    plotter.add_mesh(earth, texture = earth_texture)
    plotter.add_mesh(satellite , texture = satellite_texture)
    orbit = pv.lines_from_points(np.column_stack([x,y,z]))
    plotter.add_mesh(orbit, color = "white", line_width = 3)
    plotter.show()
    return plotter
    
# def animationPoints(r,v, no):
#     mu = 3.986004418 * 10 ** 5
#     r = np.array(r)
#     v = np.array(v)
#     rmag = mag(r)
#     vmag = mag(v)
#     h = np.cross(r,v)
#     hmag = mag(h)
#     e = (1/mu) * ((vmag**2 - mu/rmag) * r - np.dot(r,v) * v)
#     emag = mag(e) 
#     a = hmag ** 2 / (mu * (1 - emag ** 2))

#     period = 2 * np.pi * np.sqrt(a**3 / mu)
#     timesteps = np.linspace(0, period, no)
    
#     xlist = []
#     ylist = []
#     zlist = []
#     for i in range(len(timesteps)):
#         ri , vi = futurePosition(r, v, timesteps[i])
#         xlist.append(ri[0])
#         ylist.append(ri[1]) 
#         zlist.append(ri[2])

#     return xlist, ylist, zlist

# def plot_animation(xlist,ylist, zlist, r, v):
# 
#     #list to store all the screenshots
#     plots = []
#     plotter = pv.Plotter(off_screen=True)
# 
#     scale = 10
#     scale2 = 50
#     #create earth body
#     earth = pv.read("objectFiles/earth.obj")
#     earth_texture = pv.read_texture("objectFiles/earth.jpg")
#     earth = earth.scale([scale, scale, scale])
#     #create satellite body
#     satellite = pv.read("objectFiles/satellite.obj")
#     satellite = satellite.scale([scale2, scale2, scale2])
#     satellite_texture = pv.read_texture("objectFiles/satellite.png")
#     coords = orbitPlotting(r,v)
# 
#     #for loop to create plots at each timestep
#     for x,y,z in zip(xlist,ylist,zlist):
#         plotter.clear()
# 
#         #move the satellite
#         satellite = satellite.translate([x, y, z])
#         #create plots
#         plotter.background_color = "#444241"
#         plotter.add_mesh(earth, texture=earth_texture)
#         plotter.add_mesh(satellite, texture=satellite_texture)
#         orbit = pv.lines_from_points(coords)
#         plotter.add_mesh(orbit, color="white", line_width=3)
#         plotter.show(auto_close=False)
# 
#         # Gather Frames
#         plot = plotter.screenshot(return_img=True)
#         plots.append(plot)
# 
#     #create gif
#     imageio.v2.mimsave('Satellite_animation.gif', plots, duration=0.05, loop=0)
#     print('Gif saved as Satellite_animation.gif!!')
# 
# #call func
# plot_animation(x,y,z,r,v)
# 
# #plot_animation(r_array, v_array)
#orbitPlotting([8750, 5100, 0], [-3, 5.2, 5.9])     

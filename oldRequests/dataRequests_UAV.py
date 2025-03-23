## Code that uses the OSH API for Predator UAV to gather and sort data 
## Into separate .csv files

import requests
import numpy as np
import pandas

predatorUAV = 'https://api.georobotix.io/ogc/t18/api/systems/b2rju765gua3c/datastreams/' #URL of the different datastreams for the predator UAV. 

datastreamIDs = {"Platform Attitude": 'mlme3gtdfepvc',
    "Gimbal Attitude": 'mlme3gtdfepvc', 
    "Sensor Location": 'o7pce3e60s0ie'}

PAObservations = requests.get(predatorUAV + datastreamIDs["Platform Attitude"] + '/observations')
GAObservations = requests.get(predatorUAV + datastreamIDs["Gimbal Attitude"] + '/observations')
SLObservations = requests.get(predatorUAV + datastreamIDs["Sensor Location"] + '/observations')

## Sorting Planform Attitude Data into Lists
PAODict = PAObservations.json()
PAOTimestamp = []
PAOHeading = []
PAOPitch = []
PAORoll = []

for key in PAODict:
    if key == "items":
        itemsDict = PAODict[key]
        
        for item in itemsDict:
            PAOTimestamp.append(item["phenomenonTime"])
            PAOHeading.append(item["result"]['attitude']['heading'])
            PAOPitch.append(item["result"]["attitude"]['pitch'])
            PAORoll.append((item["result"]["attitude"]['roll']))
PAList = [PAOHeading, PAOPitch, PAORoll]

## Sorting Gimball Attitude Data into Lists
# This is relative to the body reference frame of the UAV, so we will use this 
# instead of the platform attutude sensor in the following calculations!
# All angles in Degrees
GAODict = GAObservations.json()
GAOtimestamp = []
GAOHeading = []
GAOPitch = []
GAORoll = []

for key in GAODict:
    if key == "items":
        itemsDict = GAODict[key]
        
        for item in itemsDict:
            GAOtimestamp.append(item["phenomenonTime"])
            GAOHeading.append(item["result"]['attitude']['heading'])
            GAOPitch.append(item["result"]["attitude"]['pitch'])
            GAORoll.append((item["result"]["attitude"]['roll']))

gaList = [GAOHeading, GAOPitch, GAORoll]
            
## Sorting Sensor Location Data into Lists
SLODict = SLObservations.json()
SLOtimestamp = []
SLOLat = [] ## Lattitude
SLOLon = [] ## Longitude
SLOAlt = [] ## Altitude
slList = [SLOLat, SLOLon, SLOAlt]

for key in SLODict:
    if key == "items":
        itemsDict = SLODict[key]
        
        for item in itemsDict:
            SLOtimestamp.append(item["phenomenonTime"])
            SLOLat.append(item["result"]["location"]['lat'])
            SLOLon.append(item["result"]["location"]['lon'])
            SLOAlt.append((item["result"]["location"]['alt']))
            
slList = [SLOLat, SLOLon, SLOAlt]

            
## Creating CSV files with the sorted data for each of the sensors!
# with open('PredatorUAV_CSV/PlanformAttitude.csv', 'w') as w:
#     for i in range(len(PAOTimestamp)):
#         if i == 0:
#              w.write("Timestamp, Heading, Pitch, Roll\n")
#         w.write(f"{PAOTimestamp[i]}, {PAOHeading[i]}, {PAOPitch[i]}, {PAORoll[i]}\n")
        
# with open('PredatorUAV_CSV/GimballAttitude.csv', 'w') as w:
#      for i in range(len(GAOtimestamp)):
#          if i == 0:
#               w.write("Timestamp, Heading, Pitch, Roll\n")
#          w.write(f"{GAOtimestamp[i]}, {GAOHeading[i]}, {GAOPitch[i]}, {GAORoll[i]}\n")   
    
# with open('PredatorUAV_CSV/SensorLocation.csv', 'w') as w:
#     for i in range(len(SLOtimestamp)):
#         if i == 0:
#              w.write("Timestamp, Lattitude, Longitude, Altitude\n")
#         w.write(f"{SLOtimestamp[i]}, {SLOLat[i]}, {SLOLon[i]}, {SLOAlt[i]}\n")
    

## Converting all of the lists to arryays!! (to do math with) 
paArray = np.transpose(np.array(PAList)) # Platform attitude Array of Heading, Roll, and Pitch
gaArray = np.transpose(np.array(gaList)) # Gimball Attitude array of heading, roll and pitch
slArray = np.transpose(np.array(slList)) # Sensor Location array of lattitude, longitude, and altitude.


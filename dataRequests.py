import requests
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
            
            
## Sorting Gimball Attitude Data into Lists
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
            
            
## Sorting Sensor Location Data into Lists
SLODict = SLObservations.json()
SLOtimestamp = []
SLOLat = [] ## Lattitude
SLOLon = [] ## Longitude
SLOAlt = [] ## Altitude

for key in SLODict:
    if key == "items":
        itemsDict = SLODict[key]
        
        for item in itemsDict:
            SLOtimestamp.append(item["phenomenonTime"])
            SLOLat.append(item["result"]["location"]['lat'])
            SLOLon.append(item["result"]["location"]['lon'])
            SLOAlt.append((item["result"]["location"]['alt']))
            
## Creating CSV files with the sorted data for each of the sensors!
with open('PlanformAttitude.csv', 'w') as w:
    for i in range(len(PAOTimestamp)):
        if i == 0:
             w.write("Timestamp, Heading, Pitch, Roll\n")
        w.write(f"{PAOTimestamp[i]}, {PAOHeading[i]}, {PAOPitch[i]}, {PAORoll[i]}\n")
        
with open('GimballAttitude.csv', 'w') as w:
     for i in range(len(GAOtimestamp)):
         if i == 0:
              w.write("Timestamp, Heading, Pitch, Roll\n")
         w.write(f"{GAOtimestamp[i]}, {GAOHeading[i]}, {GAOPitch[i]}, {GAORoll[i]}\n")   
    
with open('SensorLocation.csv', 'w') as w:
    for i in range(len(SLOtimestamp)):
        if i == 0:
             w.write("Timestamp, Lattitude, Longitude, Altitude\n")
        w.write(f"{SLOtimestamp[i]}, {SLOLat[i]}, {SLOLon[i]}, {SLOAlt[i]}\n")
    
    
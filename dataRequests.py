import requests
import json

predatorUAV = 'https://api.georobotix.io/ogc/t18/api/systems/b2rju765gua3c/datastreams/' #URL of the different datastreams for the predator UAV. 

datastreamIDs = {"Platform Attitude": 'mlme3gtdfepvc',
    "Gimbal Attitude": 'mlme3gtdfepvc', 
    "Sensor Location": 'o7pce3e60s0ie'}

PAObservations = requests.get(predatorUAV + datastreamIDs["Platform Attitude"] + '/observations')
GAObservations = requests.get(predatorUAV + datastreamIDs["Gimbal Attitude"] + '/observations')
SLObservatons = requests.get(predatorUAV + datastreamIDs["Sensor Location"] + '/observations')

PAODict = PAObservations.json()
print(PAODict["items"])

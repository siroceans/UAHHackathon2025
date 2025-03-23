# Calculate UAV stability stuff
import numpy as np
import pandas as pd
import csv
import os

# returns rudder deflection angle in degrees from UAVData.csv

def rudderDeflection():
    # ##### TEST HARNESS ####################################
    # # Create a mock UAVData.csv file with test data
    # test_data = [
    #     ["timestamp", "heading", "pitch", "roll", "time"],
    #     ["1", "10.0", "0.5", "5.0", "1.0"],
    #     ["2", "12.0", "0.6", "5.5", "2.0"],
    #     ["3", "14.0", "0.7", "6.0", "3.0"],
    #     ["4", "16.0", "0.8", "6.5", "4.0"],
    #     ["5", "18.0", "0.9", "7.0", "5.0"],
    #     ["6", "20.0", "1.0", "7.5", "6.0"],
    #     ["7", "22.0", "1.1", "8.0", "7.0"],
    #     ["8", "24.0", "1.2", "8.5", "8.0"],
    #     ["9", "26.0", "1.3", "9.0", "9.0"],
    #     ["10", "28.0", "1.4", "9.5", "10.0"],
    #     ["11", "30.0", "1.5", "10.0", "11.0"],
    #     ["12", "32.0", "1.6", "10.5", "12.0"],
    #     ["13", "34.0", "1.7", "11.0", "13.0"],
    #     ["14", "36.0", "1.8", "11.5", "14.0"],
    #     ["15", "38.0", "1.9", "12.0", "15.0"],
    #     ["16", "40.0", "2.0", "12.5", "16.0"],
    #     ["17", "42.0", "2.1", "13.0", "17.0"],
    #     ["18", "44.0", "2.2", "13.5", "18.0"],
    #     ["19", "46.0", "2.3", "14.0", "19.0"],
    #     ["20", "48.0", "2.4", "14.5", "20.0"]
    # ]

    # # Write test data to UAVData.csv
    # with open("UAVData.csv", "w", newline="") as file:
    #     writer = csv.writer(file)
    #     writer.writerows(test_data)
    # ##### TEST HARNESS ####################################

    # create matrix A and b for Boeing 747
    A1 = 0.4089
    A2 = -0.0395
    A3 = 0.0000
    A4 = -0.2454
    B = -0.2440

    # get the live data for the calculations below
    with open('UAVData.csv', "r") as csv_file:
        reader = list(csv.reader(csv_file))  # Convert reader to a list for indexing
        
        # Initialize row variables with None in case there aren’t enough rows
        last_data = second_last_data = tenth_last_data = twentieth_last_data = None

        if len(reader) >= 20:
            last_data = reader[-1]  # Last row
            second_last_data = reader[-2]  # Second-to-last row
            tenth_last_data = reader[-10]  # Tenth-to-last row
            twentieth_last_data = reader[-20]  # Twentieth-to-last row
        elif len(reader) >= 10:
            last_data = reader[-1]
            second_last_data = reader[-2]
            tenth_last_data = reader[-10]
        elif len(reader) >= 2:
            last_data = reader[-1]
            second_last_data = reader[-2]
        elif len(reader) >= 1:
            last_data = reader[-1]

    # print("Last row:", last_data)
    # print("Second to last row:", second_last_data)
    # print("Tenth to last row:", tenth_last_data)
    # print("Twentieth to last row:", twentieth_last_data)

    heading1 = float(last_data[1])
    heading2 = float(second_last_data[1])
    heading10 = float(tenth_last_data[1])
    heading20 = float(twentieth_last_data[1])

    roll1 = float(last_data[3])
    roll2 = float(second_last_data[3])
    roll10 = float(tenth_last_data[3])
    roll20 = float(twentieth_last_data[3])

    time1 = float(last_data[4])
    time2 = float(second_last_data[4])
    time10 = float(tenth_last_data[4])
    time20 = float(twentieth_last_data[4])

    # calculate states: side slip angle (betta), yaw rate (p), roll (phi), roll rate (r)
    # betta
    betta = heading1 - heading2
    # p
    p = (heading1 - heading10)/(time1 - time10)
    p1 = (heading10 - heading20)/(time10 - time20)
    # phi
    phi = roll1
    # r
    r = (roll1 - roll10)/(time1 - time10)
    r1 = (roll10 - roll20)/(time10 - time20)
    # calculate derivatives
    # betta dot
    betta_dot = p
    # p_dot
    p_dot = (p - p1)/(time1 - time20)
    # phi_dot
    phi_dot = r
    #r_dot
    r_dot = (r - r1)/(time1 - time20)

    # calculate the control input
    rudder_deflect = (r_dot - A1*betta - A2*p - A3*phi - A4*r)/B
    return(rudder_deflect)
    # ##### TEST HARNESS ####################################
    # # Clean up: remove the test CSV file after execution
    # os.remove("UAVData.csv")
    # ##### TEST HARNESS ####################################
#print(rudderDeflection())
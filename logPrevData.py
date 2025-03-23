import csv
import collections
import random
import time

# Keep track of the most recent 10,000 entries
uav_data_buffer = collections.deque(maxlen=10000)
sat_data_buffer = collections.deque(maxlen=10000)

# ##### TEST HARNESS ##########################################################
# # Mock functions to simulate data retrieval
# def getYawPitchRoll():
#     """Simulate yaw, pitch, roll readings."""
#     return [random.uniform(0, 360), random.uniform(-90, 90), random.uniform(-180, 180)],random.uniform(-1000, 1000)

# def getSatPos():
#     """Simulate satellite position (x, y, z)."""
#     return (random.uniform(-1000, 1000), random.uniform(-1000, 1000), random.uniform(-1000, 1000)), time.time()

# def getSatVel():
#     """Simulate satellite velocity (vx, vy, vz)."""
#     return (random.uniform(-10, 10), random.uniform(-10, 10), random.uniform(-10, 10)), time.time()
# ##### TEST HARNESS ###########################################################

# saves one csv file for the UAV and another for the satelite
# saves the most recent 10,000 data points for reference

def getHistoricalData():
    orientation, UAVTime = getYawPitchRoll()
    yaw, pitch, roll = orientation
    
    satPos, SatPosTime = getSatPos()
    satVel, satVelTime = getSatVel()

    prevUAVData = [yaw, pitch, roll, UAVTime]
    prevSatData = [satPos, SatPosTime, satVel, satVelTime]

    # Store in buffers (automatically removes oldest when exceeding 10,000)
    uav_data_buffer.append(prevUAVData)
    sat_data_buffer.append(prevSatData)

    # Write buffers to CSV
    writeCSV("UAVData.csv", uav_data_buffer)
    writeCSV("satData.csv", sat_data_buffer)

def writeCSV(filename, data_buffer):
    """Writes the latest 10,000 entries to the file."""
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data_buffer)

# ##### TEST HARNESS ########################################################
# # Example usage
# # Test the function by running multiple iterations
# print("Starting data logging test...")
# for i in range(10_050):  # Exceed 10,000 to test buffer limits
#     getHistoricalData()
#     if i % 1000 == 0:  # Print progress every 1,000 iterations
#         print(f"Iteration {i} complete...")

# print("Test complete. Check 'UAVData_test.csv' and 'satData_test.csv'.")
# ##### TEST HARNESS ########################################################

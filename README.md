# UAHHackathon2025
# Lequipe du Citron - UAV and Satellite Data Visualization

## Overview
Lequipe du Citron is a Python-based application designed to visualize UAV orientation data and satellite trajectories using Open Sensor Hub (OSH) data. The application provides real-time visualizations and historical data logging, making it a powerful tool for analyzing flight dynamics.

This application also includes a GIF that pulls data from the Predator UAV (MISB simulated RT) API and maps the orientation of the UAV throughout its flight using Euler angles. Euler angles describe the orientation of a rigid body, the UAV, based on its differentiation from respective axes. The data gathered from the API is presented as heading (yaw), pitch, and roll. The heading orients the UAV around the z-axis; pitch around the y-axis; and roll around the x-axis. Real-world challenges relative to this data consist of visualizing flight anomalies. Furthermore, an animation mapping the aircraft's orientation can directly display the dramatic pitch, roll, and yaw movements experienced by the aircraft.

Additionally, the application generates a visualization based on data gathered from the SPOT-6 Satellite. Upon requesting the SPOT-6 Satellite data, the API returns the satellite's location and velocity. Using only the position and velocity from the API, we can visualize the satellite's position in space, as well as map its orbital trajectory. This is done by calculating the orbital parameters for the satellite and using orbital dynamic equations like Kepler's time of flight equation and more.

## Real World Challenges Addressed
The GUI environment allows the user to view the SPOT 6 satellite's Earth track providing insight into the observable location over the Earth 
that is viewable at a given time stamp.
Additionally, the user can view the real time flight data from the Predator UAV to visualize flight anomalies that may be mission critical. Further, the GUI provides historical orientation visualization. The GUI environment provides insight into the control and stability of the UAV (assuming Boeing 747 geometry) by calculating the rudder deflection based on the state-space model and state-parameters.

## Features
- **GUI-Based Navigation**: The application is accessed through a PyQt5-based graphical interface.
- **UAV Orientation Visualization**: Real-time drone orientation tracking using Open Sensor Hub (OSH) data.
- **Satellite Trajectory Plotting**: Visualization of satellite orbits using retrieved position and velocity data.
- **Historical Data Logging**: The system logs the last 10,000 UAV orientation data points for further analysis.

## Project Structure
├── gui.py              # Main entry point that launches the GUI and integrates other components
├── uav_data.py         # Retrieves UAV heading, pitch, and roll data
├── satellite_data.py   # Retrieves satellite position and velocity
├── logger.py           # Logs historical UAV data for analysis
├── plane.py            # Handles UAV mapping functionality
├── orbit.py            # Satellite orbit plotting
├── resources/          # Contains GIFs and other media assets for the UI
└── README.md           # Project documentation

## Installation
### Prerequisites
- Python 3.8 or later
- Required Python libraries:
```sh
  pip install pyqt5 pyvistaqt matplotlib numpy pandas csv requests
```
## Usage
Run the application with:
```sh
    python gui.py
```
Since main.py is currently wrapped into gui.py, executing gui.py will launch the full application, including data retrieval and logging functionality.

## Future Development
- Code Refactoring: A dedicated main.py script should be created to serve as the primary entry point, separating GUI logic from data processing.
- Improved Modularity: Further separate concerns into well-structured modules for maintainability and scalability.
- Performance Optimizations: Enhance efficiency in data retrieval and visualization.

## Contributors
- Mares
- Brody
- Graham
- Samuel Newport

## License
This project is licensed under MIT License.

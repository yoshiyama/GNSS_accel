import sys
import pandas as pd
import pynmea2

# Get the file name from the command-line arguments
file_name = sys.argv[1]

# Define lists to hold your data
timestamp = []
lat = []
lon = []
alt = []
gps_quality = []

# Read the data line by line
with open(file_name) as f:
    content = f.read()
    lines = content.split('$')

# Parse the data
for line in lines:
    if line.startswith('GPGGA'):
        # add $ at the start of the line before parsing
        line = '$' + line
        try:
            msg = pynmea2.parse(line)
            timestamp.append(msg.timestamp)
            lat.append(msg.lat)
            lon.append(msg.lon)
            alt.append(msg.altitude)
            gps_quality.append(msg.gps_qual)
        except pynmea2.nmea.ParseError as e:
            print(f"Failed to parse line: {line}. Error: {e}")

# Create a DataFrame
df = pd.DataFrame({
    'timestamp': timestamp,
    'latitude': lat,
    'longitude': lon,
    'gps_quality': gps_quality,
    'altitude': alt
})

print(df)

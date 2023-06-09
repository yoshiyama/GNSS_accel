import sys
import pandas as pd
import pynmea2
from pyproj import Transformer
from tqdm import tqdm

# Get the file name from the command-line arguments
file_name = sys.argv[1]
output_file_name = sys.argv[2]

# Read the data line by line
with open(file_name) as f:
    content = f.read()
    lines = content.split('$')

# Create a transformer for WGS84 to JGD2000 Plane Rectangular CS IX
transformer = Transformer.from_crs("EPSG:4326", "EPSG:6675")

# Define a list to hold your data
data = []

# Parse the data
for line in tqdm(lines):
    if line.startswith('GPGGA'):
        # add $ at the start of the line before parsing
        line = '$' + line
        try:
            msg = pynmea2.parse(line)

            # Convert latitude and longitude to Plane Rectangular CS
            x, y = transformer.transform(msg.latitude, msg.longitude)

            gps_quality = int(msg.gps_qual) if msg.gps_qual is not None else 0

            # Append a new dictionary to the list
            data.append({
                'timestamp': msg.timestamp,
                'latitude': msg.latitude,
                'longitude': msg.longitude,
                'gps_quality': gps_quality,
                'altitude': msg.altitude,
                'x': x,
                'y': y
            })
        except (pynmea2.nmea.ParseError, ValueError) as e:
            print(f"Failed to parse line: {line}. Error: {e}")

# Create a DataFrame
df = pd.DataFrame(data)
df['gps_quality'] = df['gps_quality'].astype('int')

print(df)

# Save the DataFrame to a pickle file
df.to_pickle(output_file_name)

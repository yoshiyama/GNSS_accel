import sys
import pandas as pd
import pynmea2
from pyproj import Transformer
import sys
# Get the file name from the command-line arguments
file_name = sys.argv[1]

# Read the data line by line
with open(file_name) as f:
    content = f.read()
    lines = content.split('$')

# Create a transformer for WGS84 to JGD2000 Plane Rectangular CS IX
# Note: For different regions in Japan, you might need to use different Plane Rectangular CS
transformer = Transformer.from_crs("EPSG:4326", "EPSG:6675")

# Define lists to hold your data
timestamp = []
lat = []
lon = []
alt = []
gps_quality = []
# Define additional lists to hold the converted coordinates
x = []
y = []

# Parse the data
for line in lines:
    if line.startswith('GPGGA'):
        # add $ at the start of the line before parsing
        line = '$' + line
        try:
            msg = pynmea2.parse(line)

            # Convert latitude and longitude to Plane Rectangular CS
            x_, y_ = transformer.transform(msg.latitude, msg.longitude)

            # If any of the above lines fail, it won't execute the lines below

            timestamp.append(msg.timestamp)
            lat.append(msg.latitude)
            lon.append(msg.longitude)
            alt.append(msg.altitude)
            gps_quality.append(msg.gps_qual)
            x.append(x_)
            y.append(y_)
        except (pynmea2.nmea.ParseError, ValueError) as e:
            print(f"Failed to parse line: {line}. Error: {e}")


# Create a DataFrame
df = pd.DataFrame({
    'timestamp': timestamp,
    'latitude': lat,
    'longitude': lon,
    'gps_quality': gps_quality,
    'altitude': alt,
    'x': x,
    'y': y
})

print(df)
# Get the output file name from the command-line arguments
output_file_name = sys.argv[2]

# Save the DataFrame to a pickle file
df.to_pickle(output_file_name)
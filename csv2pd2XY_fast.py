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
    content = f.readlines()

# Create a transformer for WGS84 to JGD2000 Plane Rectangular CS IX
transformer = Transformer.from_crs("EPSG:4326", "EPSG:6675")

# Define a list to hold your data
data = []

# Parse the data
for i in tqdm(range(len(content))):
    line = content[i].strip()

    if line.startswith('$GPRMC'):
        try:
            msg_rmc = pynmea2.parse(line)

            gga_line = ''
            gga_found = False

            # Find the corresponding GPGGA sentence
            for j in range(i + 1, len(content)):
                gga_line = content[j].strip()
                if gga_line.startswith('$GPGGA'):
                    gga_found = True
                    break

            if not gga_found:
                continue  # Skip if GPGGA sentence is not found

            try:
                msg_gga = pynmea2.parse(gga_line)

                if msg_rmc.datestamp is None:
                    continue  # Skip if datestamp is None

                # Convert latitude and longitude to Plane Rectangular CS
                x, y = transformer.transform(msg_rmc.latitude, msg_rmc.longitude)

                gps_quality = int(msg_gga.gps_qual) if msg_gga.gps_qual is not None else 0

                # Extract year, month, and day from the datetime
                year = int(msg_rmc.datestamp.year)
                month = int(msg_rmc.datestamp.month)
                day = int(msg_rmc.datestamp.day)

                # Append a new dictionary to the list
                data.append({
                    'timestamp': msg_rmc.datetime,
                    'year': year,
                    'month': month,
                    'day': day,
                    'latitude': msg_rmc.latitude,
                    'longitude': msg_rmc.longitude,
                    'gps_quality': gps_quality,
                    'altitude': float(msg_gga.altitude) if msg_gga.altitude and msg_gga.altitude != '' else None,
                    'x': x,
                    'y': y
                })
            except (pynmea2.nmea.ParseError, ValueError) as e:
                print(f"Failed to parse GPGGA line: {gga_line}. Error: {e}")
        except (pynmea2.nmea.ParseError, ValueError) as e:
            print(f"Failed to parse GPRMC line: {line}. Error: {e}")

# Create a DataFrame
df = pd.DataFrame(data)
print(df)

# Save the DataFrame to a pickle file
df.to_pickle(output_file_name)

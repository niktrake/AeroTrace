import sys
import json
import os
import subprocess

# -----------------------------------
# ARGUMENTS
# -----------------------------------

evidence_index_path = sys.argv[1]
output_folder = sys.argv[2]

# -----------------------------------
# OUTPUT FILES
# -----------------------------------

image_locations_path = os.path.join(
    output_folder,
    "image_locations.json"
)

image_analysis_path = os.path.join(
    output_folder,
    "image_analysis.json"
)

# -----------------------------------
# LOAD EVIDENCE INDEX
# -----------------------------------

with open(evidence_index_path, "r", encoding="utf-8") as f:
    evidence_list = json.load(f)

# -----------------------------------
# RESULTS
# -----------------------------------

image_locations = []
image_analysis = []

# -----------------------------------
# KNOWN DRONE BRANDS
# -----------------------------------

KNOWN_DRONE_MAKES = [
    "DJI",
    "Autel",
    "Parrot"
]

# -----------------------------------
# PROCESS IMAGES
# -----------------------------------

for evidence in evidence_list:

    if evidence["type"] != "image":
        continue

    file_path = evidence["path"]

    if not os.path.exists(file_path):
        continue

    try:

        # -----------------------------------
        # EXIFTOOL COMMAND
        # -----------------------------------

        exiftool_path = r"C:\Tools\ExifTool\exiftool.exe"

        result = subprocess.run(
            [
                exiftool_path,
                "-j",
                file_path
            ],
            capture_output=True,
            text=True
        )

        metadata = json.loads(result.stdout)[0]

        # -----------------------------------
        # EXTRACT METADATA
        # -----------------------------------

        make = metadata.get("Make", "")
        model = metadata.get("CameraModelName", "")
        product = metadata.get("ProductName", "")

        gps_lat = metadata.get("GPSLatitude")
        gps_lon = metadata.get("GPSLongitude")

        timestamp = metadata.get("Create Date", "")

        # -----------------------------------
        # DETERMINE IMAGE TYPE
        # -----------------------------------

        image_type = "unknown_image"

        if make in KNOWN_DRONE_MAKES and model:
            image_type = "drone_capture"

        # -----------------------------------
        # SAVE ANALYSIS
        # -----------------------------------

        analysis_entry = {
            "file": os.path.basename(file_path),
            "path": file_path,
            "type": image_type,
            "make": make,
            "model": model,
            "product": product,
            "gps_available": gps_lat is not None and gps_lon is not None,
            "timestamp": timestamp
        }

        image_analysis.append(analysis_entry)

        # -----------------------------------
        # SAVE GPS IF AVAILABLE
        # -----------------------------------
        def dms_to_decimal(dms):

            try:

                dms = dms.strip()

                direction = dms[-1]

                dms = dms[:-1].strip()

                parts = (
                    dms.replace("deg", "")
                    .replace("'", "")
                    .replace('"', "")
                    .split()
            )

                degrees = float(parts[0])
                minutes = float(parts[1])
                seconds = float(parts[2])

                decimal = degrees + minutes / 60 + seconds / 3600

                if direction in ["S", "W"]:
                    decimal *= -1

                return decimal

            except Exception as e:

                print("GPS conversion error:", e)

                return None


        if gps_lat and gps_lon:

            latitude = dms_to_decimal(gps_lat)
            longitude = dms_to_decimal(gps_lon)

            if latitude is not None and longitude is not None:

                location_entry = {
                    "file": os.path.basename(file_path),
                    "latitude": latitude,
                    "longitude": longitude,
                    "timestamp": timestamp
                }

                image_locations.append(location_entry)

    except Exception as e:
        print(f"Error processing {file_path}: {e}")

# -----------------------------------
# WRITE OUTPUT FILES
# -----------------------------------

with open(image_locations_path, "w", encoding="utf-8") as f:
    json.dump(image_locations, f, indent=2)

with open(image_analysis_path, "w", encoding="utf-8") as f:
    json.dump(image_analysis, f, indent=2)

print("Image analysis completed")
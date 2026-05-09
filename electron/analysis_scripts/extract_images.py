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
        model = metadata.get("Camera Model Name", "")
        product = metadata.get("Product Name", "")

        gps_lat = metadata.get("GPS Latitude")
        gps_lon = metadata.get("GPS Longitude")

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

        if gps_lat and gps_lon:

            location_entry = {
                "file": os.path.basename(file_path),
                "latitude": gps_lat,
                "longitude": gps_lon,
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
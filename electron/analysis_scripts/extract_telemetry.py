import json
import csv
import os
import sys


# -----------------------------------
# Helper: Save JSON safely
# -----------------------------------

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


# -----------------------------------
# Extract telemetry data
# -----------------------------------

def extract_from_csv(file_path):

    gps_tracks = []

    home_point = None
    takeoff_point = None

    # Only process CSV files
    if not file_path.lower().endswith(".csv"):
        return gps_tracks, home_point, takeoff_point

    try:

        with open(
            file_path,
            "r",
            encoding="utf-8",
            errors="ignore"
        ) as csvfile:

            reader = csv.DictReader(csvfile)

            for row in reader:

                # DJI telemetry columns
                lat = row.get("IMU_ATTI(0):Latitude")

                lon = row.get("IMU_ATTI(0):Longitude")

                alt = row.get("IMU_ATTI(0):alti:D")

                pressure = row.get("IMU_ATTI(0):press:D")

                # Skip invalid rows
                if not lat or not lon:
                    continue

                try:

                    point = {
                        "latitude": float(lat),
                        "longitude": float(lon),
                        "altitude": float(alt) if alt else None,
                        "pressure": float(pressure) if pressure else None
                    }

                    gps_tracks.append(point)

                    # First valid point = takeoff point
                    if takeoff_point is None:
                        takeoff_point = point

                except:
                    continue

            # First point also acts as home point
            if len(gps_tracks) > 0:
                home_point = gps_tracks[0]

    except Exception as e:

        print(f"Error processing {file_path}: {e}")

    return gps_tracks, home_point, takeoff_point

# -----------------------------------
# MAIN
# -----------------------------------

def main():

    evidence_index_path = sys.argv[1]
    output_folder = sys.argv[2]

    with open(evidence_index_path, "r", encoding="utf-8") as f:
        evidence_list = json.load(f)

    all_tracks = []

    flight_points = []

    # Process telemetry files only
    for evidence in evidence_list:

        if evidence["type"] != "telemetry_logs":
            continue

        file_path = evidence["path"]

        gps_tracks, home_point, takeoff_point = extract_from_csv(file_path)

        if gps_tracks:

            all_tracks.append({
                "file_id": evidence["id"],
                "filename": evidence["filename"],
                "tracks": gps_tracks
            })

        if home_point or takeoff_point:

            flight_points.append({
                "file_id": evidence["id"],
                "filename": evidence["filename"],
                "home_point": home_point,
                "takeoff_point": takeoff_point
            })

    # Save outputs
    save_json(
        os.path.join(output_folder, "gps_tracks.json"),
        all_tracks
    )

    save_json(
        os.path.join(output_folder, "flight_points.json"),
        flight_points
    )

    print("Telemetry extraction complete")


if __name__ == "__main__":
    main()
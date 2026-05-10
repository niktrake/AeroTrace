import os
import sys
import json
from datetime import datetime

# =====================================
# ARGUMENTS
# =====================================

if len(sys.argv) < 2:
    print("Usage: python generate_timeline.py <analysis_folder>")
    sys.exit(1)

analysis_folder = sys.argv[1]

# =====================================
# FILE PATHS
# =====================================

gps_tracks_path = os.path.join(
    analysis_folder,
    "gps_tracks.json"
)

flight_points_path = os.path.join(
    analysis_folder,
    "flight_points.json"
)

image_locations_path = os.path.join(
    analysis_folder,
    "image_locations.json"
)

image_analysis_path = os.path.join(
    analysis_folder,
    "image_analysis.json"
)

video_analysis_path = os.path.join(
    analysis_folder,
    "video_analysis.json"
)

config_analysis_path = os.path.join(
    analysis_folder,
    "config_analysis.json"
)

timeline_output_path = os.path.join(
    analysis_folder,
    "timeline.json"
)

# =====================================
# TIMELINE STORAGE
# =====================================

timeline_events = []

# =====================================
# SAFE TIMESTAMP PARSER
# =====================================

def parse_timestamp(timestamp):

    if not timestamp:
        return None

    formats = [
        "%Y:%m:%d %H:%M:%S",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%d %H:%M:%S"
    ]

    for fmt in formats:

        try:
            return datetime.strptime(timestamp, fmt)
        except:
            continue

    return None

# =====================================
# TELEMETRY EVENTS
# =====================================

if os.path.exists(gps_tracks_path):

    with open(gps_tracks_path, "r", encoding="utf-8") as f:
        gps_data = json.load(f)

    for entry in gps_data:

        tracks = entry.get("tracks", [])

        if not tracks:
            continue

        # FIRST GPS POINT
        first_point = tracks[0]

        timeline_events.append({
            "timestamp": first_point.get("timestamp"),
            "event_type": "flight_start",
            "source": "telemetry",
            "description": "Drone takeoff detected",
            "latitude": first_point.get("latitude"),
            "longitude": first_point.get("longitude")
        })

        # LAST GPS POINT
        last_point = tracks[-1]

        timeline_events.append({
            "timestamp": last_point.get("timestamp"),
            "event_type": "flight_end",
            "source": "telemetry",
            "description": "Drone landing detected",
            "latitude": last_point.get("latitude"),
            "longitude": last_point.get("longitude")
        })

# =====================================
# FLIGHT POINT EVENTS
# =====================================

if os.path.exists(flight_points_path):

    with open(flight_points_path, "r", encoding="utf-8") as f:
        flight_points = json.load(f)

    for entry in flight_points:

        home = entry.get("home_point")

        if home:

            timeline_events.append({
                "timestamp": "",
                "event_type": "home_point",
                "source": "telemetry",
                "description": "Home point identified",
                "latitude": home.get("latitude"),
                "longitude": home.get("longitude")
            })

# =====================================
# IMAGE EVENTS
# =====================================

if os.path.exists(image_locations_path):

    with open(image_locations_path, "r", encoding="utf-8") as f:
        image_locations = json.load(f)

    for image in image_locations:

        timeline_events.append({
            "timestamp": image.get("timestamp"),
            "event_type": "image_capture",
            "source": "image",
            "description": f"Image captured: {image.get('filename')}",
            "filename": image.get("filename"),
            "latitude": image.get("latitude"),
            "longitude": image.get("longitude")
        })

# =====================================
# VIDEO EVENTS
# =====================================

if os.path.exists(video_analysis_path):

    with open(video_analysis_path, "r", encoding="utf-8") as f:
        video_analysis = json.load(f)

    for video in video_analysis:

        timeline_events.append({
            "timestamp": video.get("create_date"),
            "event_type": "video_recorded",
            "source": "video",
            "description": f"Video recorded: {video.get('filename')}",
            "filename": video.get("filename"),
            "duration": video.get("duration")
        })

# =====================================
# CONFIG EVENTS
# =====================================

if os.path.exists(config_analysis_path):

    with open(config_analysis_path, "r", encoding="utf-8") as f:
        config_analysis = json.load(f)

    for config in config_analysis:

        email = config.get(
            "DJIACCOUNTMANAGER_LASTUSEREMAIL"
        )

        if email:

            timeline_events.append({
                "timestamp": "",
                "event_type": "account_detected",
                "source": "config",
                "description": f"DJI Account detected: {email}"
            })

        last_flight = config.get(
            "Last_Flight_Record_Date_Key"
        )

        if last_flight:

            timeline_events.append({
                "timestamp": str(last_flight),
                "event_type": "last_flight_record",
                "source": "config",
                "description": "Last flight record detected"
            })

# =====================================
# SORT TIMELINE
# =====================================

timeline_events.sort(
    key=lambda x: parse_timestamp(
        x.get("timestamp")
    ) or datetime.max
)

# =====================================
# SAVE OUTPUT
# =====================================

with open(
    timeline_output_path,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        timeline_events,
        f,
        indent=2
    )

print("Timeline reconstruction completed")
print("Saved:", timeline_output_path)
import os
import sys
import json
import folium

if len(sys.argv) < 2:
    print("Usage: python generate_flight_map.py <analysis_folder>")
    sys.exit(1)

analysis_folder = sys.argv[1]

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

# =========================
# LOAD GPS TRACKS
# =========================

if not os.path.exists(gps_tracks_path):
    print("gps_tracks.json not found")
    sys.exit(1)

with open(gps_tracks_path, "r", encoding="utf-8") as f:
    gps_data = json.load(f)

flight_coordinates = []

# Extract coordinates
for file_entry in gps_data:

    tracks = file_entry.get("tracks", [])

    for point in tracks:

        lat = point.get("latitude")
        lon = point.get("longitude")

        if lat is not None and lon is not None:
            flight_coordinates.append([lat, lon])

# Safety check
if not flight_coordinates:
    print("No valid GPS coordinates found")
    sys.exit(1)

# Map center
map_center = flight_coordinates[0]

print("Total coordinates:", len(flight_coordinates))
print("Map center:", map_center)

# =========================
# CREATE MAP
# =========================

flight_map = folium.Map(
    location=map_center,
    zoom_start=17
)

# =========================
# DRAW FLIGHT PATH
# =========================

folium.PolyLine(
    flight_coordinates,
    color="blue",
    weight=4,
    opacity=0.8,
    tooltip="Flight Path"
).add_to(flight_map)

# =========================
# TAKEOFF MARKER
# =========================

start_point = flight_coordinates[0]

folium.Marker(
    location=start_point,
    popup="Takeoff Point",
    tooltip="Takeoff",
    icon=folium.Icon(color="green")
).add_to(flight_map)

# =========================
# LANDING MARKER
# =========================

end_point = flight_coordinates[-1]

folium.Marker(
    location=end_point,
    popup="Landing Point",
    tooltip="Landing",
    icon=folium.Icon(color="red")
).add_to(flight_map)

# =========================
# HOME + TAKEOFF POINTS
# =========================

if os.path.exists(flight_points_path):

    with open(flight_points_path, "r", encoding="utf-8") as f:
        flight_points = json.load(f)

    for entry in flight_points:

        home = entry.get("home_point")
        takeoff = entry.get("takeoff_point")

        # HOME POINT
        if home:

            home_lat = home.get("latitude")
            home_lon = home.get("longitude")

            if home_lat is not None and home_lon is not None:

                folium.Marker(
                    location=[home_lat, home_lon],
                    popup="Home Point",
                    tooltip="Home Point",
                    icon=folium.Icon(color="orange")
                ).add_to(flight_map)

        # TAKEOFF POINT
        if takeoff:

            takeoff_lat = takeoff.get("latitude")
            takeoff_lon = takeoff.get("longitude")

            if takeoff_lat is not None and takeoff_lon is not None:

                folium.Marker(
                    location=[takeoff_lat, takeoff_lon],
                    popup="Takeoff Coordinates",
                    tooltip="Takeoff Coordinates",
                    icon=folium.Icon(color="darkgreen")
                ).add_to(flight_map)

# =========================
# IMAGE LOCATIONS
# =========================

# =========================
# IMAGE LOCATIONS
# =========================

if os.path.exists(image_locations_path):

    with open(image_locations_path, "r", encoding="utf-8") as f:
        image_locations = json.load(f)

    print("Loaded image locations:", len(image_locations))

    for image in image_locations:

        try:

            lat = float(image.get("latitude"))
            lon = float(image.get("longitude"))

            image_name = image.get(
                "file",
                "Unknown Image"
            )

            popup_text = f"""
            <b>Image Evidence</b><br>
            Filename: {image_name}
            """

            print("Adding image marker:", image_name, lat, lon)

            folium.CircleMarker(
                location=[lat, lon],
                radius=6,
                popup=popup_text,
                tooltip=image_name,
                color="purple",
                fill=True,
                fill_color="purple",
                fill_opacity=1
            ).add_to(flight_map)

        except Exception as e:

            print("Error adding image marker:", e)

# =========================
# SAVE MAP
# =========================

output_map_path = os.path.join(
    analysis_folder,
    "flight_map.html"
)

flight_map.save(output_map_path)

print("Flight map generated successfully")
print("Saved to:", output_map_path)
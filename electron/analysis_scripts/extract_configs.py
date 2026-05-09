import os
import sys
import json
import plistlib
from datetime import datetime

# -----------------------------
# CONFIG KEYS TO EXTRACT
# -----------------------------
TARGET_KEYS = [
    "DJIACCOUNTMANAGER_LASTUSEREMAIL",
    "FIND_AIRCRAFT_LAST_LOCATION",
    "DJILastCountryCodeName",
    "Last_Flight_Record_Date_Key"
]


# -----------------------------
# CHECK DJI PLIST
# -----------------------------
def is_dji_plist(filename):

    name = filename.lower()

    return (
        "com.dji.go" in name or
        "com.dji.go.v5" in name or
        "com.dji.pilot" in name
    )


# -----------------------------
# MAIN
# -----------------------------
def main():

    if len(sys.argv) < 3:
        print("Usage: python extract_configs.py <evidence_index> <output_folder>")
        return

    evidence_index_path = sys.argv[1]
    output_folder = sys.argv[2]

    with open(evidence_index_path, "r", encoding="utf-8") as f:
        evidence_list = json.load(f)

    extracted_configs = []

    # -----------------------------
    # LOOP THROUGH EVIDENCE
    # -----------------------------
    for evidence in evidence_list:

        try:

            # only config files
            if evidence.get("type") != "configuration_file":
                continue

            file_path = evidence.get("path")
            filename = evidence.get("filename")

            # only DJI plist files
            if not is_dji_plist(filename):
                continue

            # must be plist
            if not filename.lower().endswith(".plist"):
                continue

            # file exists check
            if not os.path.exists(file_path):
                continue

            # -----------------------------
            # LOAD PLIST
            # -----------------------------
            with open(file_path, "rb") as plist_file:
                plist_data = plistlib.load(plist_file)

            config_result = {
                "source_file": filename,
                "source_evidence_id": evidence.get("id"),
                "source_path": file_path
            }

            # -----------------------------
            # EXTRACT TARGET KEYS
            # -----------------------------
            for key in TARGET_KEYS:

                value = plist_data.get(key)

                value = make_json_safe(value)

                config_result[key] = value

            extracted_configs.append(
                 make_json_safe(config_result)
            )

            print(f"Processed: {filename}")

        except Exception as e:

            print(f"Error processing {filename}: {e}")

    # -----------------------------
    # SAVE OUTPUT
    # -----------------------------
    output_path = os.path.join(
        output_folder,
        "config_analysis.json"
    )

    with open(output_path, "w", encoding="utf-8") as out_file:
        json.dump(
            extracted_configs,
            out_file,
            indent=2
        )

    print("Config extraction completed")


def make_json_safe(obj):

    # datetime -> string
    if isinstance(obj, datetime):
        return obj.isoformat()

    # bytes -> hex
    elif isinstance(obj, bytes):
        return obj.hex()

    # dictionary -> recurse
    elif isinstance(obj, dict):
        return {
            key: make_json_safe(value)
            for key, value in obj.items()
        }

    # list -> recurse
    elif isinstance(obj, list):
        return [
            make_json_safe(item)
            for item in obj
        ]

    # everything else
    else:
        return obj


# -----------------------------
# ENTRY
# -----------------------------
if __name__ == "__main__":
    main()
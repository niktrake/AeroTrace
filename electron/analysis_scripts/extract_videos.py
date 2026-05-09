import os
import sys
import json
import subprocess

# -----------------------------------
# EXIFTOOL PATH
# -----------------------------------

EXIFTOOL_PATH = r"C:\Tools\ExifTool\exiftool.exe"

# -----------------------------------
# VIDEO EXTENSIONS
# -----------------------------------

VIDEO_EXTENSIONS = [
    ".mp4",
    ".mov",
    ".avi",
    ".mkv"
]

# -----------------------------------
# RUN EXIFTOOL
# -----------------------------------

def extract_video_metadata(video_path):

    command = [
        EXIFTOOL_PATH,
        "-json",

        "-Duration",
        "-ImageWidth",
        "-ImageHeight",
        "-VideoFrameRate",
        "-AvgBitrate",
        "-Encoder",
        "-CreateDate",
        "-ModifyDate",

        video_path
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        return None

    try:
        metadata = json.loads(result.stdout)

        if len(metadata) == 0:
            return None

        return metadata[0]

    except:
        return None


# -----------------------------------
# MAIN
# -----------------------------------

def main():

    if len(sys.argv) < 3:
        print("Usage: python extract_videos.py <evidence_index> <output_folder>")
        return

    evidence_index_path = sys.argv[1]
    output_folder = sys.argv[2]

    # -----------------------------------
    # LOAD EVIDENCE INDEX
    # -----------------------------------

    with open(evidence_index_path, "r", encoding="utf-8") as f:
        evidence_list = json.load(f)

    extracted_videos = []

    # -----------------------------------
    # PROCESS FILES
    # -----------------------------------

    for evidence in evidence_list:

        try:

            if evidence.get("type") != "video":
                continue

            file_path = evidence.get("path")
            filename = evidence.get("filename")

            if not os.path.exists(file_path):
                continue

            ext = os.path.splitext(filename)[1].lower()

            if ext not in VIDEO_EXTENSIONS:
                continue

            metadata = extract_video_metadata(file_path)

            if metadata is None:
                continue

            video_result = {

                "source_file": filename,
                "source_evidence_id": evidence.get("id"),
                "source_path": file_path,

                "duration": metadata.get("Duration"),
                "width": metadata.get("ImageWidth"),
                "height": metadata.get("ImageHeight"),
                "frame_rate": metadata.get("VideoFrameRate"),
                "avg_bitrate": metadata.get("AvgBitrate"),
                "encoder": metadata.get("Encoder"),
                "create_date": metadata.get("CreateDate"),
                "modify_date": metadata.get("ModifyDate")
            }

            extracted_videos.append(video_result)

            print(f"Processed: {filename}")

        except Exception as e:

            print(f"Error processing {filename}: {e}")

    # -----------------------------------
    # SAVE OUTPUT
    # -----------------------------------

    output_path = os.path.join(
        output_folder,
        "video_analysis.json"
    )

    with open(output_path, "w", encoding="utf-8") as out_file:
        json.dump(
            extracted_videos,
            out_file,
            indent=2
        )

    print("Video analysis completed")


# -----------------------------------
# ENTRY
# -----------------------------------

if __name__ == "__main__":
    main()
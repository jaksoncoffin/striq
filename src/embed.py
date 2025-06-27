import argparse
import json
import os
import numpy as np


def load_json():
    """Load the JSON file for swing data"""

    # Ensure there is an input file
    parser = argparse.ArgumentParser(
        description="Extracts JSON information from a keypoint-extracted swing."
    )
    parser.add_argument("file_location", help="Path to the JSON swing file")
    args = parser.parse_args()

    video_path = args.file_location

    # Try to open file, handle error if there is an issue
    if not os.path.exists(video_path):
        print("The file was not found.")
        exit(1)

    with open(video_path) as f:
        data = json.load(f)

        swing_info = []

        for frame in data:
            keypoints = frame["keypoints"]
            frame_coords = []
            for kp in keypoints:
                x = kp["x"]
                y = kp["y"]
                z = kp["z"]
                frame_coords.append([x, y, z])
            swing_info.append(frame_coords)

        pose_array = np.array(swing_info)

    return pose_array


def center_pose(pose_array):
    """Center on the hips of the golfer"""

    return None

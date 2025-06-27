import os
import cv2
import argparse
import mediapipe as mp
import json


def extract_pose_keypoints():
    """Find the keypoints from a golfers swing and put the info into a JSON file"""

    # Ensure there is an input file
    parser = argparse.ArgumentParser(
        description="Extract poses from a golf swing video."
    )
    parser.add_argument("file_location", help="Path to the mp4 golf swing video")
    args = parser.parse_args()

    video_path = args.file_location

    # Try to open file, handle error if there is an issue
    if not os.path.exists(video_path):
        print("The file was not found.")
        exit(1)

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Failed to open the video.")
        exit(1)

    # Get the pose information to obtain the keypoints
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose()

    all_keypoints = []
    frame_index = 0

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(frame_rgb)

        frame_index += 1

        if results.pose_landmarks:
            keypoints = []
            for lm in results.pose_landmarks.landmark:
                keypoints.append(
                    {"x": lm.x, "y": lm.y, "z": lm.z, "visibility": lm.visibility}
                )
            all_keypoints.append({"frame": frame_index, "keypoints": keypoints})

    # Save to json output file
    output_file = "outputs/output.json"
    with open(output_file, "w") as f:
        json.dump(all_keypoints, f, indent=2)


if __name__ == "__main__":
    extract_pose_keypoints()

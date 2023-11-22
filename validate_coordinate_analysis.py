import cv2
import json
import os

def add_text_overlay(frame, text):
    # Add text overlay to the top-left corner of the frame
    font = cv2.FONT_HERSHEY_SIMPLEX
    position = (10, 30)
    font_scale = 1
    font_color = (0, 0, 255)  # Red color
    thickness = 2
    cv2.putText(frame, text, position, font, font_scale, font_color, thickness)

def create_interaction_video(input_video_path, output_video_path, json_file_path):
    # Load interaction frames from the JSON file
    with open(json_file_path, "r") as file:
        interaction_data = json.load(file)

    # Open the video file
    cap = cv2.VideoCapture(input_video_path)

    # Get video properties
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    fps = cap.get(5)

    # Create VideoWriter object to save the output video
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height))

    # Process each frame in the input video
    while True:
        ret, frame = cap.read()

        if not ret:
            break

        frame_number = int(cap.get(1))

        # Check if the current frame is an interaction frame
        if frame_number in interaction_data["interaction_frames"]:
            add_text_overlay(frame, "Interaction Detected")

        # Write the frame to the output video
        out.write(frame)

    # Release video capture and writer objects
    cap.release()
    out.release()

# Usage
input_video_path = "C:/Users/juare/OneDrive/Área de Trabalho/Work/Yale/Zimmer/Test/VideoTest1.mp4"
output_path = "C:/Users/juare/OneDrive/Área de Trabalho/Work/Yale/Zimmer/Test/Output"
output_video_path = os.path.join(output_path, "output_video_with_interaction.mp4")
json_file_path = "C:/Users/juare/OneDrive/Área de Trabalho/Work/Yale/Zimmer/Test/Output/interaction_results.json"

create_interaction_video(input_video_path, output_video_path, json_file_path)
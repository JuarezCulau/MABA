import json
import os
import numpy as np

def calculate_mse(coord1, coord2):
    # Calculate Mean Squared Error (MSE)
    return np.mean((np.array(list(coord1.values())) - np.array(list(coord2.values()))) ** 2)

def calculate_euclidean_distance(coord1, coord2):
    # Calculate Euclidean Distance
    return np.linalg.norm(np.array(list(coord1.values())) - np.array(list(coord2.values())))

def analyze_interaction(json_file_path_1, json_file_path_2, output_json_path, threshold_1, threshold_2, threshold_3):
    # Load JSON files
    with open(json_file_path_1, "r") as file:
        data_1 = json.load(file)

    with open(json_file_path_2, "r") as file:
        data_2 = json.load(file)

    # Initialize results dictionary
    interaction_frames = []

    # Ensure both JSON files have the same number of frames
    num_frames = min(len(data_1), len(data_2))

    # Initialize variable to count frames with interaction
    total_interaction_frames = 0

    for frame_number in range(num_frames):
        coordinates_1 = data_1[f"frame_{frame_number}"]
        coordinates_2 = data_2[f"frame_{frame_number}"]

        # Check for interaction using Mean Squared Error (MSE) for coordinate 1
        if coordinates_1["coordinates_1"]["x"] is not None and coordinates_2["coordinates_1"]["x"] is not None:
            mse_1 = calculate_mse(coordinates_1["coordinates_1"], coordinates_2["coordinates_1"])
            if mse_1 <= threshold_1:
                interaction_frames.append(frame_number)
                total_interaction_frames += 1

        # Check for interaction using Mean Squared Error (MSE) for coordinate 2
        elif coordinates_1["coordinates_2"]["x"] is not None and coordinates_2["coordinates_2"]["x"] is not None:
            mse_2 = calculate_mse(coordinates_1["coordinates_2"], coordinates_2["coordinates_2"])
            if mse_2 <= threshold_2:
                interaction_frames.append(frame_number)
                total_interaction_frames += 1

        # Check for interaction using Mean Squared Error (MSE) for coordinate 3
        else:
            mse_3 = calculate_mse(coordinates_1["coordinates_3"], coordinates_2["coordinates_3"])
            if mse_3 <= threshold_3:
                interaction_frames.append(frame_number)
                total_interaction_frames += 1

    # Save the results to a new JSON file
    results = {
        "interaction_frames": interaction_frames,
        "total_interaction_frames": total_interaction_frames
    }

    with open(output_json_path, "w") as output_file:
        json.dump(results, output_file)

# Usage
json_file_path_1 = "C:/Users/juare/OneDrive/Área de Trabalho/Work/Yale/Zimmer/Test/Output/coordinates_data_mother.json"
json_file_path_2 = "C:/Users/juare/OneDrive/Área de Trabalho/Work/Yale/Zimmer/Test/Output/coordinates_data_pup.json"
output_path = "C:/Users/juare/OneDrive/Área de Trabalho/Work/Yale/Zimmer/Test/Output"
output_json_path = os.path.join(output_path, "interaction_results.json")
threshold_1 = 5000  # Threshold for coordinate 1
threshold_2 = 5000  # Threshold for coordinate 2
threshold_3 = 5000  # Threshold for coordinate 3

analyze_interaction(json_file_path_1, json_file_path_2, output_json_path, threshold_1, threshold_2, threshold_3)
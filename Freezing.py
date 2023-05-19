"""
Mice Automatic Behavior Analysis (MABA)
@ Juarez Culau Batista Pires
https://github.com/JuarezCulau/MABA

Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied.  See the License for the
specific language governing permissions and limitations
under the License.
"""

import numpy as np

def calculate_distance(coord1, coord2):
    # Calculate Euclidean distance between two coordinates
    return np.sqrt((coord2[0] - coord1[0])**2 + (coord2[1] - coord1[1])**2)

def calculate_freezing_time(coordinates, threshold_distance, frame_duration):
    freezing_frames = 0
    freezing_time = 0.0

    # Iterate through the coordinates starting from the second frame
    for i in range(1, len(coordinates)):
        distance = calculate_distance(coordinates[i-1], coordinates[i])

        if distance <= threshold_distance:
            freezing_frames += 1
        else:
            # If the mouse starts moving, reset the freezing_frames counter
            freezing_frames = 0

        # Check if the consecutive freezing frames meet the required duration
        if freezing_frames >= required_freezing_frames:
            freezing_time += frame_duration

    return freezing_time

# Example Usage
coordinates = [(10, 20), (12, 22), (15, 24), (15, 24), (16, 23), (15, 24), (11, 21), (10, 20)]
threshold_distance = 2.0  # Adjust the threshold distance based on your specific case
frame_duration = 0.1  # Duration of each frame in seconds

freezing_time = calculate_freezing_time(coordinates, threshold_distance, frame_duration)
print(f"Freezing time: {freezing_time} seconds")
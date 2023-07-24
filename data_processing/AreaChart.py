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

import cv2
from coordinates import Locomotion
from data_processing.frames import Frames, Config, Analysis
import numpy as np
import matplotlib.pyplot as plt
import random

total_frames = Config.r3
time_points = list(range(total_frames))


# Function to store interaction data
def store_interaction_data(current_frame, obj1_tracked_range, obj2_tracked_range, obj3_tracked_range):
    interactions = []

    if obj1_tracked_range or obj1_tracked_range_nose:
        interactions.append({'frame': current_frame, 'object': 'Object 1'})
    if obj2_tracked_range or obj2_tracked_range_nose:
        interactions.append({'frame': current_frame, 'object': 'Object 2'})
    if obj3_tracked_range or obj3_tracked_range_nose:
        interactions.append({'frame': current_frame, 'object': 'Object 3'})

    return interactions


# Sample data for object_1, object_2, and object_3
object_1 = True
object_2 = False
object_3 = True

# Perform frame-by-frame analysis
all_interactions = []
for current_frame in time_points:
    obj1_tracked_range = object_1  # Replace this with your actual detection logic
    obj2_tracked_range = object_2  # Replace this with your actual detection logic
    obj3_tracked_range = object_3  # Replace this with your actual detection logic

    interactions = store_interaction_data(current_frame, obj1_tracked_range, obj2_tracked_range, obj3_tracked_range)
    all_interactions.extend(interactions)


# Function to convert interactions to interaction durations in frames
def convert_to_interaction_durations(interactions, total_frames):
    interaction_durations = [0] * total_frames
    for i in range(1, len(interactions)):
        prev_frame = interactions[i - 1]['frame']
        current_frame = interactions[i]['frame']
        object_interacted = interactions[i - 1]['object']
        interaction_durations[prev_frame:current_frame] = [object_interacted] * (current_frame - prev_frame)
    return interaction_durations


# Convert interactions to interaction durations in frames
interaction_durations = convert_to_interaction_durations(all_interactions, time_interval_frames)

# Separate interaction durations for each object
object1_data = [1 if interaction == 'Object 1' else 0 for interaction in interaction_durations]
object2_data = [1 if interaction == 'Object 2' else 0 for interaction in interaction_durations]
object3_data = [1 if interaction == 'Object 3' else 0 for interaction in interaction_durations]

# Create the stacked area chart
plt.stackplot(time_points, object1_data, object2_data, object3_data,
              labels=['Object 1', 'Object 2', 'Object 3'], alpha=0.7)

# Customize the plot
plt.xlabel('Frame')
plt.ylabel('Interaction')
plt.title('Interaction and Interval Time with Objects')
plt.legend(l
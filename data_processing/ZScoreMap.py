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
from data_processing.frames import Frames
from data_processing.frames import Config
from data_processing.frames import Analysis
import numpy as np
import matplotlib.pyplot as plt

def generate_zscore_map():
    # Calculate mean and standard deviation
    mean_x = np.mean(Config.CenterBodyx)
    mean_y = np.mean(Config.CenterBodyy)
    std_x = np.std(Config.CenterBodyx)
    std_y = np.std(Config.CenterBodyy)

    # Create ROI image
    RoiImg = Config.img[Locomotion.ER_QY1: Locomotion.ER_QY2, Locomotion.ER_QX1: Locomotion.ER_QX2]

    # Normalize z-score values to [0, 255]
    z_x = ((Config.CenterBodyx - mean_x) / std_x + 3) * 42.5  # Adjust the range based on your z-score range
    z_y = ((Config.CenterBodyy - mean_y) / std_y + 3) * 42.5  # Adjust the range based on your z-score range

    # Determine the size of the z-score map based on the ROI image size
    map_height, map_width = RoiImg.shape[:2]

    # Create z-score maps for x and y coordinates
    zscore_map_x = np.zeros((map_height, map_width), dtype=np.uint8)
    zscore_map_y = np.zeros((map_height, map_width), dtype=np.uint8)

    # Assign z-score values to the maps
    for x, y, z_x_val, z_y_val in zip(Config.CenterBodyx, Config.CenterBodyy, z_x, z_y):
        x_coord = int(x - Locomotion.ER_QX1)
        y_coord = int(y - Locomotion.ER_QY1)
        zscore_map_x[y_coord, x_coord] = z_x_val
        zscore_map_y[y_coord, x_coord] = z_y_val

    # Apply colormap to z-score maps
    zscore_map_x = cv2.applyColorMap(zscore_map_x, cv2.COLORMAP_JET)
    zscore_map_y = cv2.applyColorMap(zscore_map_y, cv2.COLORMAP_JET)

    # Combine x and y z-score maps
    zscore_map = cv2.addWeighted(zscore_map_x, 0.5, zscore_map_y, 0.5, 0)

    # Draw circles on z-score map
    for x, y in zip(Config.CenterBodyx, Config.CenterBodyy):
        x_coord = int(x - Locomotion.ER_QX1)
        y_coord = int(y - Locomotion.ER_QY1)
        cv2.circle(zscore_map, (x_coord, y_coord), radius=1, color=(0, 0, 255), thickness=4)

    # Display the z-score map
    cv2.imshow("Z-Score Map", zscore_map)
    cv2.waitKey(0)
    # Save z-score map
    cv2.imwrite(str(Config.projectfolder) + '/zscore_' + str(Config.sample) + '_' + str(Config.video_name) + '.jpg', zscore_map)
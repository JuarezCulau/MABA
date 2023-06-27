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

def generate_zscore_map():
    # Calculate mean and standard deviation
    mean_x = np.mean(Config.CenterBodyx)
    mean_y = np.mean(Config.CenterBodyy)
    std_x = np.std(Config.CenterBodyx)
    std_y = np.std(Config.CenterBodyy)

    # Create ROI image
    RoiImg = Config.img[Locomotion.ER_QY1: Locomotion.ER_QY2, Locomotion.ER_QX1: Locomotion.ER_QX2]

    # Create z-score map
    zscore_map = np.zeros_like(RoiImg)

    # Iterate over coordinates and z-scores
    for x, y in zip(Config.CenterBodyx, Config.CenterBodyy):
        z_x = (x - mean_x) / std_x
        z_y = (y - mean_y) / std_y

        # Convert z-scores to valid color using a colormap
        colormap = cv2.COLORMAP_JET
        color = cv2.applyColorMap(np.array([z_x, 0, z_y], dtype=np.uint8), colormap)[0, 0, :]

        # Draw circle on z-score map
        cv2.circle(zscore_map, (x, y), radius=1, color=color.tolist(), thickness=4)

    # Save z-score map
    cv2.imwrite(str(Config.projectfolder) + '/zscore_' + str(Config.sample) + '_' + str(Config.video_name) + '.jpg', zscore_map)
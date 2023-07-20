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

# Creating a copy of those coordinates because they are cleared during the cycles of the analysis
CenterBodyx_copy = []
CenterBodyy_copy = []

def generate_heatmap():
    print("460923423446356766")
    # Calculate mean and standard deviation
    mean_x = np.mean(Config.CenterBodyx)
    mean_y = np.mean(Config.CenterBodyy)
    std_x = np.std(Config.CenterBodyx)
    std_y = np.std(Config.CenterBodyy)

    # Create ROI image
    RoiImg = Config.img[Locomotion.ER_QY1: Locomotion.ER_QY2, Locomotion.ER_QX1: Locomotion.ER_QX2]

    # Normalize z-score values
    z_x = (Config.CenterBodyx - mean_x) / std_x
    z_y = (Config.CenterBodyy - mean_y) / std_y

    # Determine the size of the heatmap based on the ROI image size
    map_height, map_width = RoiImg.shape[:2]

    # Create heatmap arrays for x and y coordinates
    heatmap_x = np.zeros((map_height, map_width))
    heatmap_y = np.zeros((map_height, map_width))

    # Accumulate values in the heatmap
    for x, y, z_x_val, z_y_val in zip(Config.CenterBodyx, Config.CenterBodyy, z_x, z_y):
        x_coord = int(x - Locomotion.ER_QX1)
        y_coord = int(y - Locomotion.ER_QY1)
        heatmap_x[y_coord, x_coord] += z_x_val
        heatmap_y[y_coord, x_coord] += z_y_val

    # Apply colormap to heatmaps
    heatmap_x = plt.cm.jet(heatmap_x)
    heatmap_y = plt.cm.jet(heatmap_y)

    # Combine x and y heatmaps
    heatmap = 0.5 * heatmap_x + 0.5 * heatmap_y

    # Display the heatmap
    plt.imshow(heatmap)
    plt.colorbar()
    #plt.show()

    # Save the heatmap using plt.savefig()
    filename = str(Config.projectfolder) + '/heatmap_' + str(Config.sample) + '.jpg'
    plt.savefig(filename)

    # Save the heatmap using plt.imsave()
    full_size_filename = str(Config.projectfolder) + 'full_size_heatmap_' + str(Config.sample) + '.jpg'
    plt.imsave(full_size_filename, heatmap)
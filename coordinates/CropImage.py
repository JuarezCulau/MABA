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
from data_processing.frames import Config

def CropForAnalysis():
    global CI_QX1, CI_QX2, CI_QY1, CI_QY2, y_start, y_end, x_start, x_end
    CropROI = cv2.selectROI("(Crop Image For Analysis) Select the Entire Are of Your Experiment 'Enter'", Config.resized_image, False)

    # Adjust the ROI coordinates based on the resize ratio for the original image
    CropROI = list(CropROI)  # Convert the ROI tuple to a list

    CropROI[0] = int(CropROI[0] / Config.resize_ratio)
    CropROI[1] = int(CropROI[1] / Config.resize_ratio)
    CropROI[2] = int(CropROI[2] / Config.resize_ratio)
    CropROI[3] = int(CropROI[3] / Config.resize_ratio)

    CI_X2 = (CropROI[0]) + (CropROI[2])
    CI_Y2 = (CropROI[1]) + (CropROI[3])

    CI_1 = (CropROI[0]), (CropROI[1])
    CI_2 = CI_X2, CI_Y2
    CI_3 = (CropROI[0]), CI_Y2
    ER_4 = CI_X2, (CropROI[1])

    # Variables for zone calculation
    CI_QX1 = (CropROI[0])
    CI_QX2 = CI_X2
    CI_QY1 = (CropROI[1])
    CI_QY2 = CI_Y2


    # Extract the width and height of the ROI
    roi_width = CropROI[2]
    roi_height = CropROI[3]

    # Update the resolution of the output video
    Config.resolution = (roi_width, roi_height)
    # Crop the frame using the ROI coordinates
    y_start, y_end = CropROI[1], CropROI[1] + CropROI[3]
    x_start, x_end = CropROI[0], CropROI[0] + CropROI[2]
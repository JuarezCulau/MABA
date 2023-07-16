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
from coordinates import NOR
from data_processing.frames import Frames
from data_processing.frames import Config

# Function: generate_locomotion_graph_image
#
# Description: This function generates an image representing the complete trajectory of the mice during the video.
# It retrieves the video's resolution and creates a blank white image with the corresponding dimensions.
def CropForLocomotionGraph():
    global ER_QX1, ER_QX2, ER_QY1, ER_QY2
    ExperimentROI = cv2.selectROI("(Crop Image for Locomotion Graph) Select the Entire Are of Your Experiment 'Enter'", Config.resized_image, False)
    ER_X2 = (ExperimentROI[0]) + (ExperimentROI[2])
    ER_Y2 = (ExperimentROI[1]) + (ExperimentROI[3])

    ER_1 = (ExperimentROI[0]), (ExperimentROI[1])
    ER_2 = ER_X2, ER_Y2
    ER_3 = (ExperimentROI[0]), ER_Y2
    ER_4 = ER_X2, (ExperimentROI[1])

    # Variables for zone calculation
    ER_QX1 = (ExperimentROI[0])
    ER_QX2 = ER_X2
    ER_QY1 = (ExperimentROI[1])
    ER_QY2 = ER_Y2
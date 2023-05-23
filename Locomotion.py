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
import Config
import NOR
import Frames

#CropForLocomotionGraph creates a image with the entire path of the mice during the video.
#First it takes the resolution from the video to create a white img and here the aparatus is selected for image cut at the end.
def CropForLocomotionGraph():
    global ER_QX1, ER_QX2, ER_QY1, ER_QY2
    ExperimentROI = cv2.selectROI("(Crop Image for Locomotion Graph) Select the Entire Are of Your Experiment 'Enter'", Config.image_nl, False)
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

    if Config.SingleVideo:
        if Config.Interaction:
            NOR.SpecificObjectSelection()

        print('locomotion extract frames call')
        Frames.extractframes()

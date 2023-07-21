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
from coordinates import Locomotion
from data_processing.frames import Frames
from data_processing.frames import Config

nZones = 0
#Define Zones stores the coordinates of the four points from each ROI selected by the user
#Actually, ROI selection with OpenCV only gives one value from the point selected (x,y,w,h).
#But with only that we can acquire the coordinates of the other three points
def SelectZones():
    print('Defining Zone')
    global Z1_QX1, Z1_QX2, Z1_QY1, Z1_QY2
    global Z2_QX1, Z2_QX2, Z2_QY1, Z2_QY2
    global Z3_QX1, Z3_QX2, Z3_QY1, Z3_QY2
    global Z4_QX1, Z4_QX2, Z4_QY1, Z4_QY2
    global Z5_QX1, Z5_QX2, Z5_QY1, Z5_QY2
    global Z6_QX1, Z6_QX2, Z6_QY1, Z6_QY2
    global Z7_QX1, Z7_QX2, Z7_QY1, Z7_QY2
    global Z8_QX1, Z8_QX2, Z8_QY1, Z8_QY2
    global Z9_QX1, Z9_QX2, Z9_QY1, Z9_QY2
    global Z10_QX1, Z10_QX2, Z10_QY1, Z10_QY2
    global Z11_QX1, Z11_QX2, Z11_QY1, Z11_QY2
    global Z12_QX1, Z12_QX2, Z12_QY1, Z12_QY2


    # Zones field
    #Zone = cv2.selectROIs("Select Zones with mouse and then press 'Enter', 'Esc' to finish selection", Config.resized_image, False)
    Zone = cv2.selectROIs("Select Zones with mouse and then press 'Enter', 'Esc' to finish selection", Config.resized_image, False)

    r = 0
    # Adjust the ROI coordinates based on the resize ratio for the original image
    for roi_resized in Zone:
        ((Zone[r])[0]) = int(roi_resized[0] / Config.resize_ratio)
        ((Zone[r])[1]) = int(roi_resized[1] / Config.resize_ratio)
        ((Zone[r])[2]) = int(roi_resized[2] / Config.resize_ratio)
        ((Zone[r])[3]) = int(roi_resized[3] / Config.resize_ratio)

        r = r + 1

    global nZones

    # Small loop only to discover how many zones were selected by the user
    nZones = 0
    for i in Zone:
        nZones = nZones + 1

    #Even though this part is quite long, it will only run as many as the user selected
    #The math is the same for each zone, but I decided to not use a individual function for all the zones so that you can easily acess the individual coordinates
    #for specific experiments.
    # Zone1
    if nZones >= 1:
        Z1_X2 = ((Zone[0])[0]) + ((Zone[0])[2])
        Z1_Y2 = ((Zone[0])[1]) + ((Zone[0])[3])

        # Z is for zone, first number means which zone it is and the second number mean's which coordinate from the zone, there are four in total for each zone
        #ZX_1 is given by the default function, so there is two items with two individual sections (X, Y, W, H). By acessing X and Y you already have the first coordinate

        Z1_1 = ((Zone[0])[0]), ((Zone[0])[1])

        #
        Z1_2 = Z1_X2, Z1_Y2
        Z1_3 = ((Zone[0])[0]), Z1_Y2
        Z1_4 = Z1_X2, ((Zone[0])[1])

        # Variables for zone calculation
        # Those four are used to know the borders of the selected zone, 1 is for the beginning and 2 for the end
        #QX1 is the X coordinate already given by ROI selection
        Z1_QX1 = ((Zone[0])[0])

        #QX2 = X + W
        Z1_QX2 = Z1_X2

        #Same as with QX1, QY1 is the Y coordinate already given by ROI selection
        Z1_QY1 = ((Zone[0])[1])

        #QY2 = Y + H
        Z1_QY2 = Z1_Y2



        # Zone2
        if nZones >= 2:
            Z2_X2 = ((Zone[1])[0]) + ((Zone[1])[2])
            Z2_Y2 = ((Zone[1])[1]) + ((Zone[1])[3])

            Z2_1 = ((Zone[1])[0]), ((Zone[1])[1])
            Z2_2 = Z2_X2, Z2_Y2
            Z2_3 = ((Zone[1])[0]), Z2_Y2
            Z2_4 = Z2_X2, ((Zone[1])[1])

            # Variables for zone calculation
            Z2_QX1 = ((Zone[1])[0])
            Z2_QX2 = Z2_X2
            Z2_QY1 = ((Zone[1])[1])
            Z2_QY2 = Z2_Y2



            # Zone3
            if nZones >= 3:
                Z3_X2 = ((Zone[2])[0]) + ((Zone[2])[2])
                Z3_Y2 = ((Zone[2])[1]) + ((Zone[2])[3])

                Z3_1 = ((Zone[2])[0]), ((Zone[2])[1])
                Z3_2 = Z3_X2, Z3_Y2
                Z3_3 = ((Zone[2])[0]), Z3_Y2
                Z3_4 = Z3_X2, ((Zone[2])[1])

                # Variables for zone calculation
                Z3_QX1 = ((Zone[2])[0])
                Z3_QX2 = Z3_X2
                Z3_QY1 = ((Zone[2])[1])
                Z3_QY2 = Z3_Y2



                # Zone 4
                if nZones >= 4:
                    Z4_X2 = ((Zone[3])[0]) + ((Zone[3])[2])
                    Z4_Y2 = ((Zone[3])[1]) + ((Zone[3])[3])

                    Z4_1 = ((Zone[3])[0]), ((Zone[3])[1])
                    Z4_2 = Z4_X2, Z4_Y2
                    Z4_3 = ((Zone[3])[0]), Z4_Y2
                    Z4_4 = Z4_X2, ((Zone[3])[1])

                    # Variables for zone calculation
                    Z4_QX1 = ((Zone[3])[0])
                    Z4_QX2 = Z4_X2
                    Z4_QY1 = ((Zone[3])[1])
                    Z4_QY2 = Z4_Y2


                    # Zone 5
                    if nZones >= 5:
                        Z5_X2 = ((Zone[4])[0]) + ((Zone[4])[2])
                        Z5_Y2 = ((Zone[4])[1]) + ((Zone[4])[3])

                        Z5_1 = ((Zone[4])[0]), ((Zone[4])[1])
                        Z5_2 = Z5_X2, Z5_Y2
                        Z5_3 = ((Zone[4])[0]), Z5_Y2
                        Z5_4 = Z5_X2, ((Zone[4])[1])

                        # Variables for zone calculation
                        Z5_QX1 = ((Zone[4])[0])
                        Z5_QX2 = Z5_X2
                        Z5_QY1 = ((Zone[4])[1])
                        Z5_QY2 = Z5_Y2

                        # Zone 6
                        if nZones >= 6:
                            Z6_X2 = ((Zone[5])[0]) + ((Zone[5])[2])
                            Z6_Y2 = ((Zone[5])[1]) + ((Zone[5])[3])

                            Z6_1 = ((Zone[5])[0]), ((Zone[5])[1])
                            Z6_2 = Z6_X2, Z6_Y2
                            Z6_3 = ((Zone[5])[0]), Z6_Y2
                            Z6_4 = Z6_X2, ((Zone[5])[1])

                            # Variables for zone calculation
                            Z6_QX1 = ((Zone[5])[0])
                            Z6_QX2 = Z6_X2
                            Z6_QY1 = ((Zone[5])[1])
                            Z6_QY2 = Z6_Y2

                            # Zone7
                            if nZones >= 7:
                                Z7_X2 = ((Zone[6])[0]) + ((Zone[6])[2])
                                Z7_Y2 = ((Zone[6])[1]) + ((Zone[6])[3])

                                Z7_1 = ((Zone[6])[0]), ((Zone[6])[1])
                                Z7_2 = Z7_X2, Z7_Y2
                                Z7_3 = ((Zone[6])[0]), Z7_Y2
                                Z7_4 = Z7_X2, ((Zone[6])[1])

                                # Variables for zone calculation
                                Z7_QX1 = ((Zone[6])[0])
                                Z7_QX2 = Z7_X2
                                Z7_QY1 = ((Zone[6])[1])
                                Z7_QY2 = Z7_Y2

                                # Zone8
                                if nZones >= 8:
                                    Z8_X2 = ((Zone[7])[0]) + ((Zone[7])[2])
                                    Z8_Y2 = ((Zone[7])[1]) + ((Zone[7])[3])

                                    Z8_1 = ((Zone[7])[0]), ((Zone[7])[1])
                                    Z8_2 = Z8_X2, Z8_Y2
                                    Z8_3 = ((Zone[7])[0]), Z8_Y2
                                    Z8_4 = Z8_X2, ((Zone[7])[1])

                                    # Variables for zone calculation
                                    Z8_QX1 = ((Zone[7])[0])
                                    Z8_QX2 = Z8_X2
                                    Z8_QY1 = ((Zone[7])[1])
                                    Z8_QY2 = Z8_Y2

                                    # Zone9
                                    if nZones >= 9:
                                        Z9_X2 = ((Zone[8])[0]) + ((Zone[8])[2])
                                        Z9_Y2 = ((Zone[8])[1]) + ((Zone[8])[3])

                                        Z9_1 = ((Zone[8])[0]), ((Zone[8])[1])
                                        Z9_2 = Z9_X2, Z9_Y2
                                        Z9_3 = ((Zone[8])[0]), Z9_Y2
                                        Z9_4 = Z9_X2, ((Zone[8])[1])

                                        # Variables for zone calculation
                                        Z9_QX1 = ((Zone[8])[0])
                                        Z9_QX2 = Z9_X2
                                        Z9_QY1 = ((Zone[8])[1])
                                        Z9_QY2 = Z9_Y2

                                        # Zone10
                                        if nZones >= 10:
                                            Z10_X2 = ((Zone[9])[0]) + ((Zone[9])[2])
                                            Z10_Y2 = ((Zone[9])[1]) + ((Zone[9])[3])

                                            Z10_1 = ((Zone[9])[0]), ((Zone[9])[1])
                                            Z10_2 = Z10_X2, Z10_Y2
                                            Z10_3 = ((Zone[9])[0]), Z10_Y2
                                            Z10_4 = Z10_X2, ((Zone[9])[1])

                                            # Variables for zone calculation
                                            Z10_QX1 = ((Zone[9])[0])
                                            Z10_QX2 = Z10_X2
                                            Z10_QY1 = ((Zone[9])[1])
                                            Z10_QY2 = Z10_Y2

                                            # Zone11
                                            if nZones >= 11:
                                                Z11_X2 = ((Zone[10])[0]) + ((Zone[10])[2])
                                                Z11_Y2 = ((Zone[10])[1]) + ((Zone[10])[3])

                                                Z11_1 = ((Zone[10])[0]), ((Zone[10])[1])
                                                Z11_2 = Z11_X2, Z11_Y2
                                                Z11_3 = ((Zone[10])[0]), Z11_Y2
                                                Z11_4 = Z11_X2, ((Zone[10])[1])

                                                # Variables for zone calculation
                                                Z11_QX1 = ((Zone[10])[0])
                                                Z11_QX2 = Z11_X2
                                                Z11_QY1 = ((Zone[10])[1])
                                                Z11_QY2 = Z11_Y2

                                                # Zone12
                                                if nZones >= 12:
                                                    Z12_X2 = ((Zone[11])[0]) + ((Zone[11])[2])
                                                    Z12_Y2 = ((Zone[11])[1]) + ((Zone[11])[3])

                                                    Z12_1 = ((Zone[11])[0]), ((Zone[11])[1])
                                                    Z12_2 = Z12_X2, Z12_Y2
                                                    Z12_3 = ((Zone[11])[0]), Z12_Y2
                                                    Z12_4 = Z12_X2, ((Zone[11])[1])

                                                    # Variables for zone calculation
                                                    Z12_QX1 = ((Zone[11])[0])
                                                    Z12_QX2 = Z12_X2
                                                    Z12_QY1 = ((Zone[11])[1])
                                                    Z12_QY2 = Z12_Y2

# Note: The logic employed here is quite similar; however, in this case, we are selecting only one Region of Interest (ROI).
def SelectDualZone():
    global DZROI_QX1, DZROI_QX2, DZROI_QY1, DZROI_QY2
    dualzoneROI = cv2.selectROI("Select the Center and then press 'Enter'", Config.resized_image, False)

    # Adjust the ROI coordinates based on the resize ratio for the original image
    adjusted_dualzoneROI = [
        int(dualzoneROI[0] / Config.resize_ratio),
        int(dualzoneROI[1] / Config.resize_ratio),
        int(dualzoneROI[2] / Config.resize_ratio),
        int(dualzoneROI[3] / Config.resize_ratio)
    ]

    DZROI_X2 = adjusted_dualzoneROI[0] + adjusted_dualzoneROI[2]
    DZROI_Y2 = adjusted_dualzoneROI[1] + adjusted_dualzoneROI[3]

    DZR_1 = (adjusted_dualzoneROI[0], adjusted_dualzoneROI[1])
    DZR_2 = (DZROI_X2, DZROI_Y2)
    DZR_3 = (adjusted_dualzoneROI[0], DZROI_Y2)
    DZR_4 = (DZROI_X2, adjusted_dualzoneROI[1])

    # Variables for zone calculation
    DZROI_QX1 = adjusted_dualzoneROI[0]
    DZROI_QX2 = DZROI_X2
    DZROI_QY1 = adjusted_dualzoneROI[1]
    DZROI_QY2 = DZROI_Y2
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
import tensorflow as tf
import cv2
from data_processing.frames import Config, Frames
from coordinates import EPM, Zones, NOR, Locomotion
from data_load import Write, Model
from data_processing import Freezing, Heatmap

# Total time
r3 = 0

def ClearArrays():
    Config.RawImages.clear()

    Config.Nosex.clear()
    Config.Nosey.clear()
    Config.Headx.clear()
    Config.Heady.clear()
    Config.L_Earx.clear()
    Config.L_Eary.clear()
    Config.R_Earx.clear()
    Config.R_Eary.clear()
    Config.Body1x.clear()
    Config.Body1y.clear()
    Config.CenterBodyx.clear()
    Config.CenterBodyy.clear()
    Config.Body2x.clear()
    Config.Body2y.clear()
    Config.tail1x.clear()
    Config.tail1y.clear()
    Config.tail2x.clear()
    Config.tail2y.clear()
    Config.tail3x.clear()
    Config.tail3y.clear()
    Config.tail4x.clear()
    Config.tail4y.clear()

def selectPointEPM(TrackedPointX, TrackedPointY):
    # Check if the main point is in more than one zone at the same time, if that's the case, switch to other tracked point (V = Early State Verification)
    V_OpenArm = False
    V_ClosedArm = False
    V_Center = False

    # Check if the main point is in more than one zone at the same time, if that's the case, switch to other tracked point (V = Early State Verification)
    if cv2.pointPolygonTest(EPM.polygon_op1_umat, (TrackedPointX, TrackedPointY), False) > 0:
        V_OpenArm = True

    if cv2.pointPolygonTest(EPM.polygon_op2_umat, (TrackedPointX, TrackedPointY), False) > 0:
        V_OpenArm = True

    if cv2.pointPolygonTest(EPM.polygon_c1_umat, (TrackedPointX, TrackedPointY), False) > 0:
        V_ClosedArm = True

    if cv2.pointPolygonTest(EPM.polygon_c2_umat, (TrackedPointX, TrackedPointY), False) > 0:
        V_ClosedArm = True

    if cv2.pointPolygonTest(EPM.polygon_center_umat, (TrackedPointX, TrackedPointY), False) > 0:
        V_Center = True

    # Count the number of true variables
    true_count = sum([V_OpenArm, V_ClosedArm, V_Center])

    return (true_count)

# This is the crucial step where all the acquired values from previous steps are compiled for further analysis.
def RunSess(NoMoreFrames, codec, out):
    global r2, r3
    r2 = Config.r2
    #The model is already loaded, so I only start the session here
    print('Starting Sess')
    with tf.compat.v1.Session(graph=Model.graph) as sess:
        global r
        # Note: The variable 'r' is used in the loop to determine which image to extract from the array.
        # Additionally, the content of the arrays is cleared at the end of each session cycle.
        # Therefore, it is necessary to reset the value of 'r' to 0 at the beginning of each cycle.
        r = 0
        for i in range(len(Config.RawImages)):
            #the image is loaded here
            trackerSess = sess.run(Model.output, feed_dict={Model.input: [Config.RawImages[0 + r]]})

            print(trackerSess[0])

            # Applying a threshold to each point allows us to eliminate points tracked with low accuracy.
            Nose_T = (trackerSess[0])[2]
            Head_T = (trackerSess[1])[2]
            L_Ear_T = (trackerSess[2])[2]
            R_Ear_T = (trackerSess[3])[2]
            Body1_T = (trackerSess[4])[2]
            CenterBody_T = (trackerSess[5])[2]
            Body2_T = (trackerSess[6])[2]
            Tail1_T = (trackerSess[7])[2]
            Tail2_T = (trackerSess[8])[2]
            Tail3_T = (trackerSess[9])[2]
            Tail4_T = (trackerSess[10])[2]

            # This will be the Threshold value, between 0 and 1, selected by the user at the start.
            Threshold = Config.confiability_threshold

            # Extracting the X and Y coordinates from each tracked point is performed in this section.
            # Note that the threshold has no effect on this particular part of the code.
            Config.Nosex.append((trackerSess[0])[1])
            Config.Nosey.append((trackerSess[0])[0])
            Config.Headx.append((trackerSess[1])[1])
            Config.Heady.append((trackerSess[1])[0])
            Config.L_Earx.append((trackerSess[2])[1])
            Config.L_Eary.append((trackerSess[2])[0])
            Config.R_Earx.append((trackerSess[3])[1])
            Config.R_Eary.append((trackerSess[3])[0])
            Config.Body1x.append((trackerSess[4])[1])
            Config.Body1y.append((trackerSess[4])[0])
            Config.CenterBodyx.append((trackerSess[5])[1])
            Config.CenterBodyy.append((trackerSess[5])[0])
            Config.Body2x.append((trackerSess[6])[1])
            Config.Body2y.append((trackerSess[6])[0])
            Config.tail1x.append((trackerSess[7])[1])
            Config.tail1y.append((trackerSess[7])[0])
            Config.tail2x.append((trackerSess[8])[1])
            Config.tail2y.append((trackerSess[8])[0])
            Config.tail3x.append((trackerSess[9])[1])
            Config.tail3y.append((trackerSess[9])[0])
            Config.tail4x.append((trackerSess[10])[1])
            Config.tail4y.append((trackerSess[10])[0])

            # Multiple arrays are used to store the coordinates of each body part from each frame.
            # This allows for convenient handling and analysis of multiple body parts separately.
            # It provides an easy way to perform multiple analyses if needed.
            FrameNosex = int(Config.Nosex[r2])
            FrameNosey = int(Config.Nosey[r2])
            FrameHeadx = int(Config.Headx[r2])
            FrameHeady = int(Config.Heady[r2])
            FrameL_Earx = int(Config.L_Earx[r2])
            FrameL_Eary = int(Config.L_Eary[r2])
            FrameR_Earx = int(Config.R_Earx[r2])
            FrameR_Eary = int(Config.R_Eary[r2])
            FrameBody1x = int(Config.Body1x[r2])
            FrameBody1y = int(Config.Body1y[r2])
            FrameCenterBodyx = int(Config.CenterBodyx[r2])
            FrameCenterBodyy = int(Config.CenterBodyy[r2])
            FrameBody2x = int(Config.Body2x[r2])
            FrameBody2y = int(Config.Body2y[r2])
            Frametail1x = int(Config.tail1x[r2])
            Frametail1y = int(Config.tail1y[r2])
            Frametail2x = int(Config.tail2x[r2])
            Frametail2y = int(Config.tail2y[r2])
            Frametail3x = int(Config.tail3x[r2])
            Frametail3y = int(Config.tail3y[r2])
            Frametail4x = int(Config.tail4x[r2])
            Frametail4y = int(Config.tail4y[r2])



            # Printing the X and Y coordinates of the CenterBody on the image.
            # You can choose to print multiple points if desired, or simply remove this part as it does not affect the analysis.
            Sx = str('X: ' + str(FrameCenterBodyx))
            Sy = str('Y: ' + str(FrameCenterBodyy))

            # Only the CenterBody is being printed here. Feel free to add more body parts for printing if desired, or leave it as is.
            print(FrameCenterBodyx, FrameCenterBodyy)

            # Note: The first usage should be with the raw image.
            # Afterwards, you can utilize the local variable 'image' to draw a point at each body part marked by the model.
            image = cv2.circle(Config.RawImages[0 + r], (FrameCenterBodyx, FrameCenterBodyy), radius=1, color=(0, 0, 255), thickness=2)

            # In this section, I am feeding the image from above since it will draw over that image.
            # The code will only mark the tracked point if the precision is high enough.
            if Nose_T >= Threshold:
                image = cv2.circle(image, (FrameNosex, FrameNosey), radius=1, color=(0, 0, 255), thickness=2)
            if Head_T >= Threshold:
                image = cv2.circle(image, (FrameHeadx, FrameHeady), radius=1, color=(0, 0, 255), thickness=2)
            if L_Ear_T >= Threshold:
                image = cv2.circle(image, (FrameL_Earx, FrameL_Eary), radius=1, color=(0, 0, 255), thickness=2)
            if R_Ear_T >= Threshold:
                image = cv2.circle(image, (FrameR_Earx, FrameR_Eary), radius=1, color=(0, 0, 255), thickness=2)
            if Body1_T >= Threshold:
                image = cv2.circle(image, (FrameBody1x, FrameBody1y), radius=1, color=(0, 0, 255), thickness=2)
            if Body2_T >= Threshold:
                image = cv2.circle(image, (FrameBody2x, FrameBody2y), radius=1, color=(0, 0, 255), thickness=2)
            if Tail1_T >= Threshold:
                image = cv2.circle(image, (Frametail1x, Frametail1y), radius=1, color=(0, 0, 255), thickness=2)
            if Tail2_T >= Threshold:
                image = cv2.circle(image, (Frametail2x, Frametail2y), radius=1, color=(0, 0, 255), thickness=2)
            if Tail3_T >= Threshold:
                image = cv2.circle(image, (Frametail3x, Frametail3y), radius=1, color=(0, 0, 255), thickness=2)
            if Tail4_T >= Threshold:
                image = cv2.circle(image, (Frametail4x, Frametail4y), radius=1, color=(0, 0, 255), thickness=2)

            # Next, we draw lines between the determined points to create a skeleton-like structure.
            # This step serves a visual purpose only and does not affect any mathematical calculations or functionality.
            if Nose_T and Head_T >= Threshold:
                cv2.line(image, (FrameNosex, FrameNosey), (FrameHeadx, FrameHeady), color=(0, 0, 0), thickness=1)
            if Nose_T and L_Ear_T >= Threshold:
                cv2.line(image, (FrameNosex, FrameNosey), (FrameL_Earx, FrameL_Eary), color=(0, 0, 0), thickness=1)
            if Nose_T and R_Ear_T >= Threshold:
                cv2.line(image, (FrameNosex, FrameNosey), (FrameR_Earx, FrameR_Eary), color=(0, 0, 0), thickness=1)
            if Body1_T and R_Ear_T >= Threshold:
                cv2.line(image, (FrameR_Earx, FrameR_Eary), (FrameBody1x, FrameBody1y), color=(0, 0, 0), thickness=1)
            if Body1_T and L_Ear_T >= Threshold:
                cv2.line(image, (FrameL_Earx, FrameL_Eary), (FrameBody1x, FrameBody1y), color=(0, 0, 0), thickness=1)
            if Body1_T and Head_T >= Threshold:
                cv2.line(image, (FrameHeadx, FrameHeady), (FrameBody1x, FrameBody1y), color=(0, 0, 0), thickness=1)
            if CenterBody_T and Body1_T >= Threshold:
                cv2.line(image, (FrameCenterBodyx, FrameCenterBodyy), (FrameBody1x, FrameBody1y), color=(0, 0, 0), thickness=1)
            if CenterBody_T and Body2_T >= Threshold:
                cv2.line(image, (FrameCenterBodyx, FrameCenterBodyy), (FrameBody2x, FrameBody2y), color=(0, 0, 0), thickness=1)
            if Tail1_T and Body1_T >= Threshold:
                cv2.line(image, (Frametail1x, Frametail1y), (FrameBody2x, FrameBody2y), color=(0, 0, 0), thickness=1)
            if Tail1_T and Tail2_T >= Threshold:
                cv2.line(image, (Frametail1x, Frametail1y), (Frametail2x, Frametail2y), color=(0, 0, 0), thickness=1)
            if Tail3_T and Tail2_T >= Threshold:
                cv2.line(image, (Frametail2x, Frametail2y), (Frametail3x, Frametail3y), color=(0, 0, 0), thickness=1)
            if Tail3_T and Tail4_T >= Threshold:
                cv2.line(image, (Frametail3x, Frametail3y), (Frametail4x, Frametail4y), color=(0, 0, 0), thickness=1)

            # Putting text on the video (printing the coordinates of the CenterBody).
            # Feel free to modify the text or remove this part if it is not needed.
            cv2.putText(image, Sx, (50, 50), Config.font, 1, (0, 255, 255), 2, cv2.LINE_4)
            cv2.putText(image, Sy, (50, 100), Config.font, 1, (0, 255, 255), 2, cv2.LINE_4)

            global img
            # The variables defined here will indicate the presence of the mice in each zone for each frame.
            # These variables will be used for further calculations.
            global Zone1R, Zone2R, Zone3R,Zone4R,Zone5R,Zone6R,Zone7R,Zone8R,Zone9R,Zone10R, Zone11R, Zone12R
            global Zone1E, Zone2E, Zone3E,Zone4E,Zone5E,Zone6E,Zone7E,Zone8E,Zone9E,Zone10E, Zone11E, Zone12E
            global InsideZone1, InsideZone2, InsideZone3, InsideZone4, InsideZone5, InsideZone6, InsideZone7, InsideZone8, InsideZone9, InsideZone10, InsideZone11, InsideZone12

            # In this section, the code marks the center body on the white image for the locomotion graph.
            # You have the flexibility to easily change the point that is marked on the image by modifying this part of the code.
            if Config.CreateLocomotionGraph:
                if CenterBody_T >= Threshold:
                    cv2.circle(Config.img, (FrameCenterBodyx, FrameCenterBodyy), radius=1, color=(0, 0, 0), thickness=4)

            # The track zones analysis takes place in this section.
            # The variable ZoneXE will track the number of frames in which the mice is inside each zone,
            # and then it will be divided by the framerate to calculate the time spent in each zone.
            # This section can be easily refactored using a loop. Each zone is exposed to allow for easy modification if required for specific experiments.
            if Zones.nZones >= 1:
                if (Zones.Z1_QX1 <= FrameCenterBodyx <= Zones.Z1_QX2) and (Zones.Z1_QY1 <= FrameCenterBodyy <= Zones.Z1_QY2):
                    cv2.putText(image, 'Mice in Zone 1!!!', (50, 200), Config.font, 1, (0, 255, 255), 2, cv2.LINE_4)
                    Config.Zone1R = Config.Zone1R + 1

                    if not Config.InsideZone1:
                        Config.Zone1E = Config.Zone1E + 1
                        Config.InsideZone1 = True
                        Config.InsideZone2 = False
                        Config.InsideZone3 = False
                        Config.InsideZone4 = False
                        Config.InsideZone5 = False
                        Config.InsideZone6 = False
                        Config.InsideZone7 = False
                        Config.InsideZone8 = False
                        Config.InsideZone9 = False
                        Config.InsideZone10 = False
                        Config.InsideZone11 = False
                        Config.InsideZone12 = False

                if Zones.nZones >= 2:
                    if (Zones.Z2_QX1 <= FrameCenterBodyx <= Zones.Z2_QX2) and (Zones.Z2_QY1 <= FrameCenterBodyy <= Zones.Z2_QY2):
                        cv2.putText(image, 'Mice in Zone 2!!!', (50, 200), Config.font, 1, (0, 255, 255), 2, cv2.LINE_4)
                        Config.Zone2R = Config.Zone2R + 1

                        if not Config.InsideZone2:
                            Config.Zone2E = Config.Zone2E + 1
                            Config.InsideZone1 = False
                            Config.InsideZone2 = True
                            Config.InsideZone3 = False
                            Config.InsideZone4 = False
                            Config.InsideZone5 = False
                            Config.InsideZone6 = False
                            Config.InsideZone7 = False
                            Config.InsideZone8 = False
                            Config.InsideZone9 = False
                            Config.InsideZone10 = False
                            Config.InsideZone11 = False
                            Config.InsideZone12 = False

                    if Zones.nZones >= 3:
                        if (Zones.Z3_QX1 <= FrameCenterBodyx <= Zones.Z3_QX2) and (Zones.Z3_QY1 <= FrameCenterBodyy <= Zones.Z3_QY2):
                            cv2.putText(image, 'Mice in Zone 3!!!', (50, 200), Config.font, 1, (0, 255, 255), 2, cv2.LINE_4)
                            Config.Zone3R = Config.Zone3R + 1

                            if not Config.InsideZone3:
                                Config.Zone3E = Config.Zone3E + 1
                                Config.InsideZone1 = False
                                Config.InsideZone2 = False
                                Config.InsideZone3 = True
                                Config.InsideZone4 = False
                                Config.InsideZone5 = False
                                Config.InsideZone6 = False
                                Config.InsideZone7 = False
                                Config.InsideZone8 = False
                                Config.InsideZone9 = False
                                Config.InsideZone10 = False
                                Config.InsideZone11 = False
                                Config.InsideZone12 = False

                        if Zones.nZones >= 4:
                             if (Zones.Z4_QX1 <= FrameCenterBodyx <= Zones.Z4_QX2) and (Zones.Z4_QY1 <= FrameCenterBodyy <= Zones.Z4_QY2):
                                cv2.putText(image, 'Mice in Zone 4!!!', (50, 200), Config.font, 1, (0, 255, 255), 2, cv2.LINE_4)
                                Config.Zone4R = Config.Zone4R + 1

                                if not Config.InsideZone4:
                                    Config.Zone4E = Config.Zone4E + 1
                                    Config.InsideZone1 = False
                                    Config.InsideZone2 = False
                                    Config.InsideZone3 = False
                                    Config.InsideZone4 = True
                                    Config.InsideZone5 = False
                                    Config.InsideZone6 = False
                                    Config.InsideZone7 = False
                                    Config.InsideZone8 = False
                                    Config.InsideZone9 = False
                                    Config.InsideZone10 = False
                                    Config.InsideZone11 = False
                                    Config.InsideZone12 = False

                             if Zones.nZones >= 5:
                                if (Zones.Z5_QX1 <= FrameCenterBodyx <= Zones.Z5_QX2) and (Zones.Z5_QY1 <= FrameCenterBodyy <= Zones.Z5_QY2):
                                    cv2.putText(image, 'Mice in Zone 5!!!', (50, 200), Config.font, 1, (0, 255, 255), 2, cv2.LINE_4)
                                    Config.Zone5R = Config.Zone5R + 1

                                    if not Config.InsideZone5:
                                        Config.Zone5E = Config.Zone5E + 1
                                        Config.InsideZone1 = False
                                        Config.InsideZone2 = False
                                        Config.InsideZone3 = False
                                        Config.InsideZone4 = False
                                        Config.InsideZone5 = True
                                        Config.InsideZone6 = False
                                        Config.InsideZone7 = False
                                        Config.InsideZone8 = False
                                        Config.InsideZone9 = False
                                        Config.InsideZone10 = False
                                        Config.InsideZone11 = False
                                        Config.InsideZone12 = False

                                if Zones.nZones >= 6:
                                    if (Zones.Z6_QX1 <= FrameCenterBodyx <= Zones.Z6_QX2) and (Zones.Z6_QY1 <= FrameCenterBodyy <= Zones.Z6_QY2):
                                        cv2.putText(image, 'Mice in Zone 6!!!', (50, 200), Config.font, 1, (0, 255, 255), 2, cv2.LINE_4)
                                        Config.Zone6R = Config.Zone6R + 1

                                        if not Config.InsideZone6:
                                            Config.Zone6E = Config.Zone6E + 1
                                            Config.InsideZone1 = False
                                            Config.InsideZone2 = False
                                            Config.InsideZone3 = False
                                            Config.InsideZone4 = False
                                            Config.InsideZone5 = False
                                            Config.InsideZone6 = True
                                            Config.InsideZone7 = False
                                            Config.InsideZone8 = False
                                            Config.InsideZone9 = False
                                            Config.InsideZone10 = False
                                            Config.InsideZone11 = False
                                            Config.InsideZone12 = False

                                    if Zones.nZones >= 7:
                                        if (Zones.Z7_QX1 <= FrameCenterBodyx <= Zones.Z7_QX2) and (Zones.Z7_QY1 <= FrameCenterBodyy <= Zones.Z7_QY2):
                                            cv2.putText(image, 'Mice in Zone 7!!!', (50, 200), Config.font, 1, (0, 255, 255), 2, cv2.LINE_4)
                                            Config.Zone7R = Config.Zone7R + 1

                                            if not Config.InsideZone7:
                                                Config.Zone7E = Config.Zone7E + 1
                                                Config.InsideZone1 = False
                                                Config.InsideZone2 = False
                                                Config.InsideZone3 = False
                                                Config.InsideZone4 = False
                                                Config.InsideZone5 = False
                                                Config.InsideZone6 = False
                                                Config.InsideZone7 = True
                                                Config.InsideZone8 = False
                                                Config.InsideZone9 = False
                                                Config.InsideZone10 = False
                                                Config.InsideZone11 = False
                                                Config.InsideZone12 = False

                                        if Zones.nZones >= 8:
                                            if (Zones.Z8_QX1 <= FrameCenterBodyx <= Zones.Z8_QX2) and (Zones.Z8_QY1 <= FrameCenterBodyy <= Zones.Z8_QY2):
                                                cv2.putText(image, 'Mice in Zone 8!!!', (50, 200), Config.font, 1, (0, 255, 255), 2, cv2.LINE_4)
                                                Config.Zone8R = Config.Zone8R + 1

                                                if not Config.InsideZone8:
                                                    Config.Zone8E = Config.Zone8E + 1
                                                    Config.InsideZone1 = False
                                                    Config.InsideZone2 = False
                                                    Config.InsideZone3 = False
                                                    Config.InsideZone4 = False
                                                    Config.InsideZone5 = False
                                                    Config.InsideZone6 = False
                                                    Config.InsideZone7 = False
                                                    Config.InsideZone8 = True
                                                    Config.InsideZone9 = False
                                                    Config.InsideZone10 = False
                                                    Config.InsideZone11 = False
                                                    Config.InsideZone12 = False

                                            if Zones.nZones >= 9:
                                                if (Zones.Z9_QX1 <= FrameCenterBodyx <= Zones.Z9_QX2) and (Zones.Z9_QY1 <= FrameCenterBodyy <= Zones.Z9_QY2):
                                                    cv2.putText(image, 'Mice in Zone 9!!!', (50, 200), Config.font, 1, (0, 255, 255), 2, cv2.LINE_4)
                                                    Config.Zone9R = Config.Zone9R + 1

                                                    if not Config.InsideZone9:
                                                        Config.Zone9E = Config.Zone9E + 1
                                                        Config.InsideZone1 = False
                                                        Config.InsideZone2 = False
                                                        Config.InsideZone3 = False
                                                        Config.InsideZone4 = False
                                                        Config.InsideZone5 = False
                                                        Config.InsideZone6 = False
                                                        Config.InsideZone7 = False
                                                        Config.InsideZone8 = False
                                                        Config.InsideZone9 = True
                                                        Config.InsideZone10 = False
                                                        Config.InsideZone11 = False
                                                        Config.InsideZone12 = False

                                                if Zones.nZones >= 10:
                                                    if (Zones.Z10_QX1 <= FrameCenterBodyx <= Zones.Z10_QX2) and (Zones.Z10_QY1 <= FrameCenterBodyy <= Zones.Z10_QY2):
                                                        cv2.putText(image, 'Mice in Zone 10!!!', (50, 200), Config.font, 1, (0, 255, 255), 2, cv2.LINE_4)
                                                        Config.Zone10R = Config.Zone10R + 1

                                                        if not Config.InsideZone10:
                                                            Config.Zone10E = Config.Zone10E + 1
                                                            Config.InsideZone1 = False
                                                            Config.InsideZone2 = False
                                                            Config.InsideZone3 = False
                                                            Config.InsideZone4 = False
                                                            Config.InsideZone5 = False
                                                            Config.InsideZone6 = False
                                                            Config.InsideZone7 = False
                                                            Config.InsideZone8 = False
                                                            Config.InsideZone9 = False
                                                            Config.InsideZone10 = True
                                                            Config.InsideZone11 = False
                                                            Config.InsideZone12 = False

                                                    if Zones.nZones >= 11:
                                                        if (Zones.Z11_QX1 <= FrameCenterBodyx <= Zones.Z11_QX2) and (Zones.Z11_QY1 <= FrameCenterBodyy <= Zones.Z11_QY2):
                                                            cv2.putText(image, 'Mice in Zone 11!!!', (50, 200), Config.font, 1, (0, 255, 255), 2, cv2.LINE_4)
                                                            Config.Zone11R = Config.Zone11R + 1

                                                            if not Config.InsideZone11:
                                                                Config.Zone11E = Config.Zone11E + 1
                                                                Config.InsideZone1 = False
                                                                Config.InsideZone2 = False
                                                                Config.InsideZone3 = False
                                                                Config.InsideZone4 = False
                                                                Config.InsideZone5 = False
                                                                Config.InsideZone6 = False
                                                                Config.InsideZone7 = False
                                                                Config.InsideZone8 = False
                                                                Config.InsideZone9 = False
                                                                Config.InsideZone10 = False
                                                                Config.InsideZone11 = True
                                                                Config.InsideZone12 = False

                                                        if Zones.nZones >= 12:
                                                            if (Zones.Z12_QX1 <= FrameCenterBodyx <= Zones.Z12_QX2) and (Zones.Z12_QY1 <= FrameCenterBodyy <= Zones.Z12_QY2):
                                                                cv2.putText(image, 'Mice in Zone 12!!!', (50, 200), Config.font, 1, (0, 255, 255), 2, cv2.LINE_4)
                                                                Config.Zone12R = Config.Zone12R + 1

                                                                if not Config.InsideZone12:
                                                                    Config.Zone12E = Config.Zone12E + 1
                                                                    Config.InsideZone1 = False
                                                                    Config.InsideZone2 = False
                                                                    Config.InsideZone3 = False
                                                                    Config.InsideZone4 = False
                                                                    Config.InsideZone5 = False
                                                                    Config.InsideZone6 = False
                                                                    Config.InsideZone7 = False
                                                                    Config.InsideZone8 = False
                                                                    Config.InsideZone9 = False
                                                                    Config.InsideZone10 = False
                                                                    Config.InsideZone11 = False
                                                                    Config.InsideZone12 = True

            # Similar to the trackzone analysis, but this time with only one zone.
            # The value from the other zone is subtracted from the duration of the video in this case.
            global DZR
            if Config.DualZone:
                if (Zones.DZROI_QX1 <= FrameCenterBodyx <= Zones.DZROI_QX2) and (Zones.DZROI_QY1 <= FrameCenterBodyy <= Zones.DZROI_QY2):
                    cv2.putText(image, 'Mice at Center!!!', (50, 400), Config.font, 1, (0, 255, 255), 2, cv2.LINE_4)
                    Config.DZR = Config.DZR + 1

                else:
                    cv2.putText(image, 'Mice at Periphery!!!', (50, 400), Config.font, 1, (0, 255, 255), 2, cv2.LINE_4)

            # Analyzing the area around the object (Novel Object Recognition)
            global FirstObjectR, SecondObjectR, Interaction_FirstObjectR, Interaction_SecondObjectR, N_OBJ_1, N_OBJ_2
            if Config.NovelObject:
                if (NOR.R1_QX1 <= FrameCenterBodyx <= NOR.R1_QX2) and (NOR.R1_QY1 <= FrameCenterBodyy <= NOR.R1_QY2):
                    cv2.putText(image, 'Close to object 1!!!', (50, 300), Config.font, 1, (0, 255, 255), 2, cv2.LINE_4)
                    Config.FirstObjectR = Config.FirstObjectR + 1

                if (NOR.R2_QX1 <= FrameCenterBodyx <= NOR.R2_QX2) and (NOR.R2_QY1 <= FrameCenterBodyy <= NOR.R2_QY2):
                    cv2.putText(image, 'Close to object 2!!!', (50, 300), Config.font, 1, (0, 255, 255), 2, cv2.LINE_4)
                    Config.SecondObjectR = Config.SecondObjectR + 1

                # If the user is analyzing the area around the object and decides to crop the video only for the moments when the mice are close to the object,
                # it allows them to visually inspect whether the mice are interacting with the object, but with a smaller video size.
                if Config.CropRon:
                    if (NOR.R2_QX1 <= FrameCenterBodyx <= NOR.R2_QX2) and (NOR.R2_QY1 <= FrameCenterBodyy <= NOR.R2_QY2) or (NOR.R1_QX1 <= FrameCenterBodyx <= NOR.R1_QX2) and (
                            NOR.R1_QY1 <= FrameCenterBodyy <= NOR.R1_QY2):
                        # If CropRon is selected, the code will write only the frames when the mice are close enough to any object.
                        out.write(image)


                # This section focuses on analyzing the interaction with the object based on nose proximity.
                if Config.Interaction:
                    if (NOR.OBJ1_QX1 <= FrameNosex <= NOR.OBJ1_QX2) and (NOR.OBJ1_QY1 <= FrameNosey <= NOR.OBJ1_QY2):
                        cv2.putText(image, 'Interacting with object 1!!!', (50, 250), Config.font, 1, (0, 255, 255), 2, cv2.LINE_4)

                        # Time of interaction with each object
                        Config.Interaction_FirstObjectR = Config.Interaction_FirstObjectR + 1

                        # This one is for the number of interactions with each object
                        if not Config.I_OBJ_1:
                            Config.I_OBJ_1 = True
                            Config.N_OBJ_1 = Config.N_OBJ_1 + 1

                    if (NOR.OBJ2_QX1 <= FrameNosex <= NOR.OBJ2_QX2) and (NOR.OBJ2_QY1 <= FrameNosey <= NOR.OBJ2_QY2):
                        cv2.putText(image, 'Interacting with object 2!!!', (50, 250), Config.font, 1, (0, 255, 255), 2, cv2.LINE_4)
                        Config.Interaction_SecondObjectR = Config.Interaction_SecondObjectR + 1

                        if not Config.I_OBJ_2:
                            Config.I_OBJ_2 = True
                            Config.N_OBJ_2 = Config.N_OBJ_2 + 1

                    if not (NOR.OBJ1_QX1 <= FrameNosex <= NOR.OBJ1_QX2) and (NOR.OBJ1_QY1 <= FrameNosey <= NOR.OBJ1_QY2):
                        Config.I_OBJ_1 = False

                    if not (NOR.OBJ2_QX1 <= FrameNosex <= NOR.OBJ2_QX2) and (NOR.OBJ2_QY1 <= FrameNosey <= NOR.OBJ2_QY2):
                        Config.I_OBJ_2 = False

            # In this section, we check if the mice is freezing.
            # Each additional body part being considered adds more frames to the threshold.
            # For example, if there are 60 frames per second and two body parts being counted, each body part adds one frame.
            # Therefore, in this case, even though half a second would be 30 frames, for two body parts, it should be 60 frames for half a second.
            if Config.Freeze:
                threshold_frames = 30
                threshold_distance = 3

                if Head_T >= Threshold:

                    # First check the head for freezing
                    ComparisonCoordinates = [(int(Config.Headx[r2]), int(Config.Heady[r2])), (int(Config.Headx[r2 - 1]), int(Config.Heady[r2 - 1]))]
                    if threshold_frames < Freezing.calculate_freezing_time(ComparisonCoordinates, threshold_distance):
                        cv2.putText(image, 'Freezing', (50, 280), Config.font, 1, (0, 255, 255), 2, cv2.LINE_4)

                        Config.freezing_frames_total = Config.freezing_frames_total + 1

                        if not Config.FreezeState:
                            Config.N_Freezing = Config.N_Freezing + 1
                            Config.FreezeState = True

                            # Add the time when freezing started
                            Config.freezing_frames_total = Config.freezing_frames_total + threshold_frames

                            # Check if there is an interval between freezing
                            if Config.IntervalFreezing > 120:
                                Config.N_IntervalFreezing = Config.N_IntervalFreezing + 1

                        Config.IntervalFreezing = 0

                    else:
                        Config.FreezeState = False
                        Config.IntervalFreezing = Config.IntervalFreezing + 1

                if CenterBody_T >= Threshold:
                    # Second, check the Centerbody for freezing
                    ComparisonCoordinates = [(int(Config.CenterBodyx[r2]), int(Config.CenterBodyy[r2])), (int(Config.CenterBodyx[r2 - 1]), int(Config.CenterBodyy[r2 - 1]))]
                    if threshold_frames < Freezing.calculate_freezing_time(ComparisonCoordinates, threshold_distance):
                        cv2.putText(image, 'Freezing', (50, 280), Config.font, 1, (0, 255, 255), 2, cv2.LINE_4)

                        Config.freezing_frames_total = Config.freezing_frames_total + 1

                        if not Config.FreezeState:
                            Config.N_Freezing = Config.N_Freezing + 1
                            Config.FreezeState = True

                            # Add the time when freezing started
                            Config.freezing_frames_total = Config.freezing_frames_total + threshold_frames

                            # Check if there is an interval between freezing
                            if Config.IntervalFreezing > 120:
                                Config.N_IntervalFreezing = Config.N_IntervalFreezing + 1

                        Config.IntervalFreezing = 0

                    else:
                        Config.FreezeState = False
                        Config.IntervalFreezing = Config.IntervalFreezing + 1

                if Nose_T >= Threshold:
                    # Thirdly, we check for nose movement. In this case, the nose is only used to determine if freezing should be cancelled.
                    ComparisonCoordinates = [(int(Config.Nosex[r2]), int(Config.Nosey[r2])), (int(Config.Nosex[r2 - 1]), int(Config.Nosey[r2 - 1]))]
                    if not threshold_frames < Freezing.nose_movement(ComparisonCoordinates, threshold_distance):
                        Config.FreezeState = False
                        Config.IntervalFreezing = Config.IntervalFreezing + 1

            # Elevated cross maze analysis
            if Config.EPM:
                TrackedPointX = FrameCenterBodyx
                TrackedPointY = FrameCenterBodyy

                # Set the nose confidence
                confidence_nose = Nose_T >= Threshold

                # Set Nose Range
                op1_nose_range = cv2.pointPolygonTest(EPM.polygon_op1_umat, (FrameNosex, FrameNosey), False) < 0
                op2_nose_range = cv2.pointPolygonTest(EPM.polygon_op2_umat, (FrameNosex, FrameNosey), False) < 0
                c1_nose_range = cv2.pointPolygonTest(EPM.polygon_c1_umat, (FrameNosex, FrameNosey), False) < 0
                c2_nose_range = cv2.pointPolygonTest(EPM.polygon_c2_umat, (FrameNosex, FrameNosey), False) < 0
                center_nose_range = cv2.pointPolygonTest(EPM.polygon_center_umat, (FrameNosex, FrameNosey), False) < 0

                # Check the location of tracked point and availability for the analysis
                if selectPointEPM(TrackedPointX, TrackedPointY) >= 2:
                    TrackedPointX = FrameBody1x
                    TrackedPointY = FrameBody1y

                    if selectPointEPM(TrackedPointX, TrackedPointY) >= 2:
                        TrackedPointX = FrameHeadx
                        TrackedPointY = FrameHeady

                        if selectPointEPM(TrackedPointX, TrackedPointY) >= 2:
                            TrackedPointX = FrameCenterBodyx
                            TrackedPointY = FrameCenterBodyy

                # Set Tracked Point Range
                op1_tracked_range = cv2.pointPolygonTest(EPM.polygon_op1_umat, (TrackedPointX, TrackedPointY), False) > 0
                op2_tracked_range = cv2.pointPolygonTest(EPM.polygon_op2_umat, (TrackedPointX, TrackedPointY), False) > 0
                c1_tracked_range = cv2.pointPolygonTest(EPM.polygon_c1_umat, (TrackedPointX, TrackedPointY), False) > 0
                c2_tracked_range = cv2.pointPolygonTest(EPM.polygon_c2_umat, (TrackedPointX, TrackedPointY), False) > 0
                center_tracked_range = cv2.pointPolygonTest(EPM.polygon_center_umat, (TrackedPointX, TrackedPointY), False) > 0

                # Check if the point is inside the rectangle
                if op1_tracked_range:
                    # Add one frame to the time without interval for this zone
                    Config.IT_OpenArm = Config.IT_OpenArm + 1

                    if Config.S_OpenArm:
                        cv2.putText(image, 'Open Arm 1', (50, 300), Config.font, 1, (0, 255, 255), 2, cv2.LINE_4)

                        # Add one frame to the total time in this zone
                        Config.T_OpenArm = Config.T_OpenArm + 1

                    # Check if is already inside before adding another entry
                    if not Config.S_OpenArm and Config.IT_OpenArm >= 15:
                        # Add one entry
                        Config.N_OpenArm = Config.N_OpenArm + 1

                        # Set the states of the other zones to false and this one to true
                        Config.S_ClosedArm = False
                        Config.S_Center = False
                        Config.S_OpenArm = True

                        # Set the Time without interval in the other zones to 0
                        Config.IT_ClosedArm = 0
                        Config.IT_Center = 0
                        cv2.putText(image, 'Open Arm 1', (50, 300), Config.font, 1, (0, 255, 255), 2, cv2.LINE_4)

                        # Add the interval count to the total time
                        Config.T_OpenArm = Config.T_OpenArm + Config.IT_OpenArm

                    # Check nose location
                    if confidence_nose and Config.S_OpenArm and (op1_nose_range and center_nose_range):

                        cv2.putText(image, 'Nose Outside', (50, 270), Config.font, 1, (0, 255, 255), 2, cv2.LINE_4)
                        Config.T_NoseOutside = Config.T_NoseOutside + 1

                        if not Config.S_NoseOutside and Config.T_NoseInside >= 60:
                            Config.T_NoseInside = 0
                            Config.N_NoseOutside = Config.N_NoseOutside + 1
                            Config.S_NoseOutside = True

                    else:
                        Config.S_NoseOutside = False
                        Config.T_NoseInside = Config.T_NoseInside + 1

                if op2_tracked_range:
                    Config.IT_OpenArm = Config.IT_OpenArm + 1

                    if Config.S_OpenArm:
                        cv2.putText(image, 'Open Arm 2', (50, 300), Config.font, 1, (0, 255, 255), 2, cv2.LINE_4)

                        # Add one frame to thte total time in this zone
                        Config.T_OpenArm = Config.T_OpenArm + 1

                    # Check if is already inside before adding another entry
                    if not Config.S_OpenArm and Config.IT_OpenArm >= 15:
                        Config.N_OpenArm = Config.N_OpenArm + 1
                        Config.S_ClosedArm = False
                        Config.S_Center = False
                        Config.S_OpenArm = True
                        Config.IT_ClosedArm = 0
                        Config.IT_Center = 0
                        cv2.putText(image, 'Open Arm 2', (50, 300), Config.font, 1, (0, 255, 255), 2, cv2.LINE_4)
                        # Add the interval count to the total time
                        Config.T_OpenArm = Config.T_OpenArm + Config.IT_OpenArm

                    # Check nose location
                    if confidence_nose and Config.S_OpenArm and (op2_nose_range and center_nose_range):
                        cv2.putText(image, 'Nose Outside', (50, 270), Config.font, 1, (0, 255, 255), 2, cv2.LINE_4)
                        Config.T_NoseOutside = Config.T_NoseOutside + 1

                        if not Config.S_NoseOutside and Config.T_NoseInside >= 60:
                            Config.T_NoseInside = 0
                            Config.N_NoseOutside = Config.N_NoseOutside + 1
                            Config.S_NoseOutside = True

                    else:
                        Config.S_NoseOutside = False
                        Config.T_NoseInside = Config.T_NoseInside + 1

                if c1_tracked_range:
                    # Additionally, we include the time with the nose inside in this part since there is no check for the nose outside at the closed arms.
                    Config.T_NoseInside = Config.T_NoseInside + 1
                    Config.IT_ClosedArm = Config.IT_ClosedArm + 1

                    if Config.S_ClosedArm:
                        cv2.putText(image, 'Closed Arm 1', (50, 300), Config.font, 1, (0, 255, 255), 2, cv2.LINE_4)

                        # Add the interval count to the total time
                        Config.T_ClosedArm = Config.T_ClosedArm + 1

                    # Check if is already inside before adding another entry
                    if not Config.S_ClosedArm and Config.IT_ClosedArm >= 15:
                        Config.N_ClosedArm = Config.N_ClosedArm + 1
                        Config.S_Center = False
                        Config.S_OpenArm = False
                        Config.S_ClosedArm = True
                        Config.IT_OpenArm = 0
                        Config.IT_Center = 0
                        cv2.putText(image, 'Closed Arm 1', (50, 300), Config.font, 1, (0, 255, 255), 2, cv2.LINE_4)
                        Config.T_ClosedArm = Config.T_ClosedArm + Config.IT_ClosedArm

                if c2_tracked_range:
                    # Additionally, we include the time with the nose inside in this part since there is no check for the nose outside at the closed arms.
                    Config.T_NoseInside = Config.T_NoseInside + 1
                    Config.IT_ClosedArm = Config.IT_ClosedArm + 1

                    if Config.S_ClosedArm:
                        cv2.putText(image, 'Closed Arm 2', (50, 300), Config.font, 1, (0, 255, 255), 2, cv2.LINE_4)

                        # Add the interval count to the total time
                        Config.T_ClosedArm = Config.T_ClosedArm + 1

                    # Check if is already inside before adding another entry
                    if not Config.S_ClosedArm and Config.IT_ClosedArm >= 15:
                        Config.N_ClosedArm = Config.N_ClosedArm + 1
                        Config.S_Center = False
                        Config.S_OpenArm = False
                        Config.S_ClosedArm = True
                        Config.IT_OpenArm = 0
                        Config.IT_Center = 0
                        cv2.putText(image, 'Closed Arm 2', (50, 300), Config.font, 1, (0, 255, 255), 2, cv2.LINE_4)
                        Config.T_ClosedArm = Config.T_ClosedArm + Config.IT_ClosedArm

                if center_tracked_range:
                    Config.IT_Center = Config.IT_Center + 1

                    if Config.S_Center:
                        cv2.putText(image, 'Center', (50, 300), Config.font, 1, (0, 255, 255), 2, cv2.LINE_4)
                        Config.T_Center = Config.T_Center + 1

                    # Check if is already inside before adding another entry, since there is no much time in the center, it is reduced (5)
                    if not Config.S_Center and Config.IT_Center >= 5:
                        Config.N_Center = Config.N_Center + 1
                        Config.S_OpenArm = False
                        Config.S_ClosedArm = False
                        Config.S_Center = True
                        Config.IT_OpenArm = 0
                        Config.IT_ClosedArm = 0
                        cv2.putText(image, 'Center', (50, 300), Config.font, 1, (0, 255, 255), 2, cv2.LINE_4)
                        Config.T_Center = Config.T_Center + Config.IT_Center


                    # Check nose location
                    # In this case, I am checking if the nose is outside every zone, not just the center zone.
                    if confidence_nose and Config.S_Center and (center_nose_range and c1_nose_range and c2_nose_range and op1_nose_range and op2_nose_range):

                        cv2.putText(image, 'Nose Outside Arm (Center)', (50, 270), Config.font, 1, (0, 255, 255), 2, cv2.LINE_4)
                        Config.T_NoseOutside = Config.T_NoseOutside + 1

                        if not Config.S_NoseOutside and Config.T_NoseInside >= 60:
                            Config.T_NoseInside = 0
                            Config.N_NoseOutside = Config.N_NoseOutside + 1
                            Config.S_NoseOutside = True

                    else:
                        Config.S_NoseOutside = False
                        Config.T_NoseInside = Config.T_NoseInside + 1

            # If CropRon was not selected, the code will write the video at each loop iteration.
            if not Config.CropRon:
                out.write(image)

            r += 1
            r2 += 1
            r3 += 1

        # If there are no more frames, the code will clear the RawImages variable one last time and call the next function, "WriteFile".
        if NoMoreFrames:
            #Check if it should generate a heatmap
            if Config.Heatmap:
                Heatmap.CenterBodyx_copy.extend(Config.CenterBodyx)
                Heatmap.CenterBodyy_copy.extend(Config.CenterBodyy)
                Heatmap.generate_heatmap()

            ClearArrays()
            out.release
            print('Video Created')
            Write.writeFile()

            # Reset total number of frames to zero
            r3 = 0

        # If there are more frames, the code will clear the RawImages variable and return to the extractframes loop until there are no more frames remaining.
        else:

            # Make a copy of the center coordinates before clearing it
            if Config.Heatmap:
                Heatmap.CenterBodyx_copy.extend(Config.CenterBodyx)
                Heatmap.CenterBodyy_copy.extend(Config.CenterBodyy)

            ClearArrays()
            print('clearing array extract frames call')
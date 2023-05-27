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

import tensorflow as tf
import cv2
import Config
import Model
import Frames
import Zones
import NOR
import Locomotion
import Write
import Freezing

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


#This is where magic happens, every value acquired so far is compiled here for the analysis
def RunSess(NoMoreFrames, codec, out):
    global r2
    r2 = Config.r2
    #The model is already loaded, so I only start the session here
    print('Starting Sess')
    with tf.compat.v1.Session(graph=Model.graph) as sess:
        global r
        #r is used in the loop to know what image to take from the array, the content of the arrays is also cleaned at the end of the sess at each cycle
        #Then, r must be defined as 0 once again.
        r = 0
        for i in range(len(Config.RawImages)):
            #the image is loaded here
            trackerSess = sess.run(Model.output, feed_dict={Model.input: [Config.RawImages[0 + r]]})

            print(trackerSess[0])

            #lets apply a threshold for each point, that way we can eliminate points tracked with low acurracy
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

            #this will be the Threshold value, between 0 and 1.
            Threshold = 0.95

            #here we extract the X and Y coordinate from each tracked point. The threshold have no function in this part.
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

#Multiple arrays for each body part are going story the coordinates from each frame. A easy way to run multiple analysis if you need it.
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



            #The coordinates X, Y from the CenterBody will be printed in the image, you can print multiple points if you want or just remove this part, it plays no role on the analysis.
            Sx = str('X: ' + str(FrameCenterBodyx))
            Sy = str('Y: ' + str(FrameCenterBodyy))

            #I am only printing the centerBody here, print more if you want or leave the way it is
            print(FrameCenterBodyx, FrameCenterBodyy)

            #first one must use raw image, after that use local variable 'image' to draw a point at each body part marked by the model
            image = cv2.circle(Config.RawImages[0 + r], (FrameCenterBodyx, FrameCenterBodyy), radius=1, color=(0, 0, 255), thickness=2)

            #I am feeding the image from above here since it will draw over that image
            #It will only mark the point tracked if the precision is high enough. Please remember, the default is 0.8.
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


            #Now let's draw a line between determined points to work as a skeleton, it has visual purpose only and it will not affect any math or anything like that
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


            # put text (I am printing on video the coord of the centerbody, change it if you like it or remove if you don't need it
            cv2.putText(image, Sx, (50, 50), Config.font, 1, (0, 255, 255), 2, cv2.LINE_4)
            cv2.putText(image, Sy, (50, 100), Config.font, 1, (0, 255, 255), 2, cv2.LINE_4)

            global img
            #the variables down here will mark the presence of the mice at each zone in the frame and use it for further calculations
            global Zone1R, Zone2R, Zone3R,Zone4R,Zone5R,Zone6R,Zone7R,Zone8R,Zone9R,Zone10R, Zone11R, Zone12R
            global Zone1E, Zone2E, Zone3E,Zone4E,Zone5E,Zone6E,Zone7E,Zone8E,Zone9E,Zone10E, Zone11E, Zone12E
            global InsideZone1, InsideZone2, InsideZone3, InsideZone4, InsideZone5, InsideZone6, InsideZone7, InsideZone8, InsideZone9, InsideZone10, InsideZone11, InsideZone12

            #Here it will mark the center body at the white img, for the locomotion graph. You can easily changing the point marked on the image here!
            if Config.CreateLocomotionGraph:
                cv2.circle(Config.img, (FrameCenterBodyx, FrameCenterBodyy), radius=1, color=(0, 0, 0), thickness=4)

            #Track zones analysis happens here.
            #ZoneXE will mark the number of frames that the mice is inside each zone and then divide it by the framerate to acquire the time inside each zone.
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

            #Same thing from trackzone, but this time with only one zone, the value from the other one is substracted from the duration of the video.
            global DZR
            if Config.DualZone:
                if (Zones.DZROI_QX1 <= FrameCenterBodyx <= Zones.DZROI_QX2) and (Zones.DZROI_QY1 <= FrameCenterBodyy <= Zones.DZROI_QY2):
                    cv2.putText(image, 'Mice at Center!!!', (50, 400), Config.font, 1, (0, 255, 255), 2, cv2.LINE_4)
                    Config.DZR = Config.DZR + 1

                else:
                    cv2.putText(image, 'Mice at Periphery!!!', (50, 400), Config.font, 1, (0, 255, 255), 2, cv2.LINE_4)

            #Analyzing the area around the object
            global FirstObjectR, SecondObjectR, Interaction_FirstObjectR, Interaction_SecondObjectR, N_OBJ_1, N_OBJ_2
            if Config.NovelObject:
                if (NOR.R1_QX1 <= FrameCenterBodyx <= NOR.R1_QX2) and (NOR.R1_QY1 <= FrameCenterBodyy <= NOR.R1_QY2):
                    cv2.putText(image, 'Close to object 1!!!', (50, 300), Config.font, 1, (0, 255, 255), 2, cv2.LINE_4)
                    Config.FirstObjectR = Config.FirstObjectR + 1

                if (NOR.R2_QX1 <= FrameCenterBodyx <= NOR.R2_QX2) and (NOR.R2_QY1 <= FrameCenterBodyy <= NOR.R2_QY2):
                    cv2.putText(image, 'Close to object 2!!!', (50, 300), Config.font, 1, (0, 255, 255), 2, cv2.LINE_4)
                    Config.SecondObjectR = Config.SecondObjectR + 1

                #if the user is analyzing the area around the object and decide to crop the video only for the moments when the mice is close to the object
                #that way he can decide with his own eyes if the mice is inracting with the object, but with a smaller video
                if Config.CropRon:
                    if (NOR.R2_QX1 <= FrameCenterBodyx <= NOR.R2_QX2) and (NOR.R2_QY1 <= FrameCenterBodyy <= NOR.R2_QY2) or (NOR.R1_QX1 <= FrameCenterBodyx <= NOR.R1_QX2) and (
                            NOR.R1_QY1 <= FrameCenterBodyy <= NOR.R1_QY2):
                        #if CropRon is selected, then the video is going to write only the frames when the mice is close enough to any object.
                        out.write(image)


                #Analyzing the interaction with the object by nose proximity
                if Config.Interaction:
                    if (NOR.OBJ1_QX1 <= FrameNosex <= NOR.OBJ1_QX2) and (NOR.OBJ1_QY1 <= FrameNosey <= NOR.OBJ1_QY2):
                        cv2.putText(image, 'Interacting with object 1!!!', (50, 250), Config.font, 1, (0, 255, 255), 2, cv2.LINE_4)

                        #Time of interaction with each object
                        Config.Interaction_FirstObjectR = Config.Interaction_FirstObjectR + 1

                        #now this one is for the number of interactions with each object
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

            #Check if the mice is freezing
            #Each body part added should add more frames to threshold
            #Example: there is 60 frames per second, but since there is two body parts being counted, each one of them is going to add one frame
            #So in this case, even though half a second would be 30 frames, for 2 body parts, it should be 60 frames for half a second
            if Config.Freeze:
                threshold_frames = 30
                threshold_distance = 3

                if Head_T >= Threshold:

                    #First check the head for freezing
                    ComparisonCoordinates = [(int(Config.Headx[r2]), int(Config.Heady[r2])), (int(Config.Headx[r2 - 1]), int(Config.Heady[r2 - 1]))]
                    if threshold_frames < Freezing.calculate_freezing_time(ComparisonCoordinates, threshold_distance):
                        cv2.putText(image, 'Freezing', (50, 280), Config.font, 1, (0, 255, 255), 2, cv2.LINE_4)

                        Config.freezing_frames_total = Config.freezing_frames_total + 1

                        if not Config.FreezeState:
                            Config.N_Freezing = Config.N_Freezing + 1
                            Config.FreezeState = True

                            # Check if there is an interval between freezing
                            if Config.IntervalFreezing > 120:
                                Config.N_IntervalFreezing = Config.N_IntervalFreezing + 1

                        Config.IntervalFreezing = 0

                    else:
                        Config.FreezeState = False
                        Config.IntervalFreezing = Config.IntervalFreezing + 1

                if CenterBody_T >= Threshold:
                    #Second, check the centerbody for freezing
                    ComparisonCoordinates = [(int(Config.CenterBodyx[r2]), int(Config.CenterBodyy[r2])), (int(Config.CenterBodyx[r2 - 1]), int(Config.CenterBodyy[r2 - 1]))]
                    if threshold_frames < Freezing.calculate_freezing_time(ComparisonCoordinates, threshold_distance):
                        cv2.putText(image, 'Freezing', (50, 280), Config.font, 1, (0, 255, 255), 2, cv2.LINE_4)

                        Config.freezing_frames_total = Config.freezing_frames_total + 1

                        if not Config.FreezeState:
                            Config.N_Freezing = Config.N_Freezing + 1
                            Config.FreezeState = True

                            # Check if there is an interval between freezing
                            if Config.IntervalFreezing > 120:
                                Config.N_IntervalFreezing = Config.N_IntervalFreezing + 1

                        Config.IntervalFreezing = 0

                    else:
                        Config.FreezeState = False
                        Config.IntervalFreezing = Config.IntervalFreezing + 1

                if Nose_T >= Threshold:
                    #Third, check for nose movement, in this case the nose is going to be used only to cancel the freezing
                    ComparisonCoordinates = [(int(Config.Nosex[r2]), int(Config.Nosey[r2])), (int(Config.Nosex[r2 - 1]), int(Config.Nosey[r2 - 1]))]
                    if not threshold_frames < Freezing.nose_movement(ComparisonCoordinates, threshold_distance):
                        Config.FreezeState = False
                        Config.IntervalFreezing = Config.IntervalFreezing + 1


            #if CropRon was not selected, then it will write the video at each loop
            if not Config.CropRon:
                out.write(image)

            r = r + 1
            r2 = r2 + 1

        #if there is no more frames, then it will clear the RawImages one last time and call the next function "WriteFile"
        if NoMoreFrames:
            ClearArrays()
            out.release
            print('Video Created')
            Write.writeFile()

        #If there is more frames, then it will clear the RawImages and go back into the extractframes loop until there is no more frames.
        else:
            ClearArrays()
            print('clearing array extract frames call')
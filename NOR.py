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

import Frames
import cv2
import Config
import Locomotion

#this function will track the mice when he is close to the object but it will not determine interaction,
# the specific object selection determine interaction but for that, the model must have precision enough to track the nose of the mice in your video
#I choose the same logic from the trackzones, this time for only two objects, if for some reason there is more objects in your experiment, then expand here!
def ObjectSelection():
    RON = cv2.selectROIs("select the area around the objects", Config.image_nl, False)
    global R1_X2, R1_Y2, R1_1, R1_2, R1_3, R1_4, R1_QX1, R1_QX2, R1_QY1, R1_QY2
    global R2_X2, R2_Y2, R2_1, R2_2, R2_3, R2_4, R2_QX1, R2_QX2, R2_QY1, R2_QY2
    #First Object
    R1_X2 = ((RON[0])[0]) + ((RON[0])[2])
    R1_Y2 = ((RON[0])[1]) + ((RON[0])[3])

    # Z is for zone, first number means which zone it is and the second number mean's which coordinate from the zone, there are four in total for each zone
    #This one retain the value of the four points selected at each zone, I will leave a example of how to use those values below (Example 1)
    R1_1 = ((RON[0])[0]), ((RON[0])[1])
    R1_2 = R1_X2, R1_Y2
    R1_3 = ((RON[0])[0]), R1_Y2
    R1_4 = R1_X2, ((RON[0])[1])

    # Variables for zone calculation
    R1_QX1 = ((RON[0])[0])
    R1_QX2 = R1_X2
    R1_QY1 = ((RON[0])[1])
    R1_QY2 = R1_Y2

    #Example 1
    #Example function mentioned above | This is going to create a image with the four points of the zone around the object
    # First click coordinate
    #cv2.circle(image_nl, (R1_1), radius=20, color=(0, 0, 255), thickness=10)
    # release click coordinate
    #cv2.circle(image_nl, (R1_2), radius=20, color=(0, 0, 255), thickness=10)
    #cv2.circle(image_nl, (R1_3), radius=20, color=(0, 0, 255), thickness=10)
    #cv2.circle(image_nl, (R1_4), radius=20, color=(0, 0, 255), thickness=10)
    #cv2.imwrite('Object 1.jpg', image_nl)

    #Second Object
    R2_X2 = ((RON[1])[0]) + ((RON[1])[2])
    R2_Y2 = ((RON[1])[1]) + ((RON[1])[3])

    # Z is for zone, first nome means which zone it is and the second number mean's which coordinate from the zone, there are four in total for each zone
    R2_1 = ((RON[1])[0]), ((RON[1])[1])
    R2_2 = R2_X2, R2_Y2
    R2_3 = ((RON[1])[0]), R2_Y2
    R2_4 = R2_X2, ((RON[1])[1])

    # Variables for zone calculation
    R2_QX1 = ((RON[1])[0])
    R2_QX2 = R2_X2
    R2_QY1 = ((RON[1])[1])
    R2_QY2 = R2_Y2

    if Config.CreateLocomotionGraph:
        Locomotion.CropForLocomotionGraph()

    if Config.Interaction:
        SpecificObjectSelection()

    if not Config.CreateLocomotionGraph and not Config.Interaction:
        print('object selection extract frames call')
        Frames.extractframes()

#this function will be used to track the close proximity to the object
#is important to remember that this functio will only work properly if the model has accuracy enough to track the nose of your mice
#That said, test the model in video or train a new pb model, if you have accuracy to track the nose, then use this function.
# The threshold is being set at 0.8, I recommend to use a higher value if you have trained a new model with your own images and with good resolution
#You can also decrease the threshold, but I don't recommend.
def SpecificObjectSelection():
    OBJ = cv2.selectROIs("Select the Objects, press 'Enter' after selecting the first one, 'Esc' After selecting the second", Config.image_nl, False)
    global OBJ1_X2, OBJ1_Y2, OBJ1_1, OBJ1_2, OBJ1_3, OBJ1_4, OBJ1_QX1, OBJ1_QX2, OBJ1_QY1, OBJ1_QY2
    global OBJ2_X2, OBJ2_Y2, OBJ2_1, OBJ2_2, OBJ2_3, OBJ2_4, OBJ2_QX1, OBJ2_QX2, OBJ2_QY1, OBJ2_QY2
    #First Object
    OBJ1_X2 = ((OBJ[0])[0]) + ((OBJ[0])[2])
    OBJ1_Y2 = ((OBJ[0])[1]) + ((OBJ[0])[3])

    # Z is for zone, first nome means which zone it is and the second number mean's which coordinate from the zone, there are four in total for each zone
    OBJ1_1 = ((OBJ[0])[0]), ((OBJ[0])[1])
    OBJ1_2 = OBJ1_X2, OBJ1_Y2
    OBJ1_3 = ((OBJ[0])[0]), OBJ1_Y2
    OBJ1_4 = OBJ1_X2, ((OBJ[0])[1])

    # Variables for zone calculation
    OBJ1_QX1 = ((OBJ[0])[0])
    OBJ1_QX2 = OBJ1_X2
    OBJ1_QY1 = ((OBJ[0])[1])
    OBJ1_QY2 = OBJ1_Y2

    #Second Object
    OBJ2_X2 = ((OBJ[1])[0]) + ((OBJ[1])[2])
    OBJ2_Y2 = ((OBJ[1])[1]) + ((OBJ[1])[3])

    # Z is for zone, first nome means which zone it is and the second number mean's which coordinate from the zone, there are four in total for each zone
    OBJ2_1 = ((OBJ[1])[0]), ((OBJ[1])[1])
    OBJ2_2 = OBJ2_X2, OBJ2_Y2
    OBJ2_3 = ((OBJ[1])[0]), OBJ2_Y2
    OBJ2_4 = OBJ2_X2, ((OBJ[1])[1])

    # Variables for zone calculation
    OBJ2_QX1 = ((OBJ[1])[0])
    OBJ2_QX2 = OBJ2_X2
    OBJ2_QY1 = ((OBJ[1])[1])
    OBJ2_QY2 = OBJ2_Y2

    print('specific obj extract frames')
    Frames.extractframes()
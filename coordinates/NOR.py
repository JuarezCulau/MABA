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

# Description: This function tracks the mice when it is in close proximity to an object, but it does not determine interaction.
# The interaction is determined by the specific object selection. To track the mice's nose accurately in the video, the model
# needs to have sufficient precision.
#
# Approach: The function follows a similar logic as the track_zones function, but in this case, it is designed to track only two objects.
# If there are more objects in your experiment, you can expand this section accordingly.
def ObjectSelection():
    RON = cv2.selectROIs("select the area around the objects, press 'Enter' after selecting the first one, 'Esc' After selecting the second", Config.image_nl, False)
    global R1_X2, R1_Y2, R1_1, R1_2, R1_3, R1_4, R1_QX1, R1_QX2, R1_QY1, R1_QY2
    global R2_X2, R2_Y2, R2_1, R2_2, R2_3, R2_4, R2_QX1, R2_QX2, R2_QY1, R2_QY2
    #First Object
    R1_X2 = ((RON[0])[0]) + ((RON[0])[2])
    R1_Y2 = ((RON[0])[1]) + ((RON[0])[3])

    # Description: Z stands for zone. The first number indicates which zone it is, and the second number represents the coordinate within the zone. There are a total of four coordinates for each zone.
    #
    # Usage: This variable retains the values of the four points selected for each zone. There is an example (Example 1)
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

    R2_1 = ((RON[1])[0]), ((RON[1])[1])
    R2_2 = R2_X2, R2_Y2
    R2_3 = ((RON[1])[0]), R2_Y2
    R2_4 = R2_X2, ((RON[1])[1])

    # Variables for zone calculation
    R2_QX1 = ((RON[1])[0])
    R2_QX2 = R2_X2
    R2_QY1 = ((RON[1])[1])
    R2_QY2 = R2_Y2

# Description: This function is used to track the close proximity of the object. It's important to note that this function will only work properly if the model has sufficient accuracy to track the nose of the mice.
#
# Usage: Before using this function, it is recommended to test the model on a video or train a new model (pb model) to ensure accurate nose tracking. Adjust the threshold value accordingly.
def SpecificObjectSelection():
    print('58063865036')
    OBJ = cv2.selectROIs("Select the Objects, press 'Enter' after selecting the first one, 'Esc' After selecting the second", Config.image_nl, False)
    global OBJ1_X2, OBJ1_Y2, OBJ1_1, OBJ1_2, OBJ1_3, OBJ1_4, OBJ1_QX1, OBJ1_QX2, OBJ1_QY1, OBJ1_QY2
    global OBJ2_X2, OBJ2_Y2, OBJ2_1, OBJ2_2, OBJ2_3, OBJ2_4, OBJ2_QX1, OBJ2_QX2, OBJ2_QY1, OBJ2_QY2
    #First Object
    OBJ1_X2 = ((OBJ[0])[0]) + ((OBJ[0])[2])
    OBJ1_Y2 = ((OBJ[0])[1]) + ((OBJ[0])[3])

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

    OBJ2_1 = ((OBJ[1])[0]), ((OBJ[1])[1])
    OBJ2_2 = OBJ2_X2, OBJ2_Y2
    OBJ2_3 = ((OBJ[1])[0]), OBJ2_Y2
    OBJ2_4 = OBJ2_X2, ((OBJ[1])[1])

    # Variables for zone calculation
    OBJ2_QX1 = ((OBJ[1])[0])
    OBJ2_QX2 = OBJ2_X2
    OBJ2_QY1 = ((OBJ[1])[1])
    OBJ2_QY2 = OBJ2_Y2
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
import os

import numpy as np
import tensorflow as tf
import cv2
from data_processing.frames import Config, Frames
from coordinates import EPM, Zones, NOR, Locomotion
from data_load import Write, Model
from data_processing import Freezing, Heatmap
import json

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

# Initialize an empty dictionary to store coordinates
coordinates_data = {}

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
            CenterBody_T = (trackerSess[2])[2]

            # This will be the Threshold value, between 0 and 1, selected by the user at the start.
            Threshold = Config.confiability_threshold

            # Extracting the X and Y coordinates from each tracked point is performed in this section.
            # Note that the threshold has no effect on this particular part of the code.
            Config.Nosex.append((trackerSess[0])[1])
            Config.Nosey.append((trackerSess[0])[0])
            Config.Headx.append((trackerSess[1])[1])
            Config.Heady.append((trackerSess[1])[0])
            Config.CenterBodyx.append((trackerSess[2])[1])
            Config.CenterBodyy.append((trackerSess[2])[0])

            # Multiple arrays are used to store the coordinates of each body part from each frame.
            # This allows for convenient handling and analysis of multiple body parts separately.
            # It provides an easy way to perform multiple analyses if needed.
            FrameNosex = int(Config.Nosex[r2])
            FrameNosey = int(Config.Nosey[r2])
            FrameHeadx = int(Config.Headx[r2])
            FrameHeady = int(Config.Heady[r2])
            FrameCenterBodyx = int(Config.CenterBodyx[r2])
            FrameCenterBodyy = int(Config.CenterBodyy[r2])

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

            # Putting text on the video (printing the coordinates of the CenterBody).
            # Feel free to modify the text or remove this part if it is not needed.
            cv2.putText(image, Sx, (50, 50), Config.font, 1, (0, 255, 255), 2, cv2.LINE_4)
            cv2.putText(image, Sy, (50, 100), Config.font, 1, (0, 255, 255), 2, cv2.LINE_4)

            global img

            # Zimmer Analysis (Save Coordinates)


            if Nose_T >= Threshold:
                coordinates_1 = {"x": FrameNosex, "y": FrameNosey}
            else:
                coordinates_1 = {"x": None, "y": None}

            if Head_T >= Threshold:
                coordinates_2 = {"x": FrameHeadx, "y": FrameHeady}
            else:
                coordinates_2 = {"x": None, "y": None}

            # Create a dictionary for the current frame
            frame_data = {
                "frame_number": r2,
                "coordinates_1": coordinates_1,
                "coordinates_2": coordinates_2,
                "coordinates_3": {"x": FrameCenterBodyx, "y": FrameCenterBodyy},
            }

            # Add the frame data to the overall dictionary
            coordinates_data[f"frame_{r}"] = frame_data


            # In this section, the code marks the center body on the white image for the locomotion graph.
            # You have the flexibility to easily change the point that is marked on the image by modifying this part of the code.
            if Config.CreateLocomotionGraph:
                if CenterBody_T >= Threshold:
                    cv2.circle(Config.img, (FrameCenterBodyx, FrameCenterBodyy), radius=1, color=(0, 0, 0), thickness=4)

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

            # Zimmer Coordinates!
            # Specify the path for the JSON file
            json_file_path = os.path.join(Config.projectfolder, "coordinates_data.json")

            # Save the coordinates data to the JSON file
            with open(json_file_path, "w") as json_file:
                json.dump(coordinates_data, json_file)

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
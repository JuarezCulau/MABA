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
import cv2
import Config
import GUI
from sys import getsizeof
import Analysis
import CropImage

#The analysis is made in cycles.
#Usually tensorflow is loaded for each frame, as a unique session. I am not using that way because it takes too long to load a new session each time for each frame
#Instead, extractframes stores a chunk of images into a array and then a session is loaded only one time for the entire array.
#Using that method creates a memory problem.
#--------------------------
#Tensors starts to take too much video memory. This can be a problem even with several GPUs.
#This is not a problem if your video has low resolution or if it's not that long, but if you have great resolution and or hours of video, then it would require too much video memory.
#So we extract the frames in cycles, reducing the number of time a session is loaded from each frame to once each 2k frames or something close to that
#You can also increase that number if you have memory enough and want to save a few seconds
import NOR
import Zones

def convert_to_int(value):
    return int(value) if value is not None else None

def ExtractCoordinatestxt(video_name):
    # Construct the file path of the corresponding text file
    txt_file_path = Config.projectfolder + '/info_' + video_name + ".txt"

    # Check if the text file exists
    if not os.path.exists(txt_file_path):
        print(f"Text file '{txt_file_path}' does not exist.")
        return

    else:
        # Read the variables from the text file
        variables = {}
        with open(txt_file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if line.startswith("#"):
                    continue  # Skip commented lines
                if "=" in line:
                    variable_name, value = line.split("=")
                    variable_name = variable_name.strip()
                    value = value.strip()
                    variables[variable_name] = value

        # Get the specific variables and update the coordinates with it

        #Zones ROI Coordinates
        Zones.nZones = convert_to_int(variables.get("nZones"))

        Zones.Z1_QX1 = convert_to_int(variables.get("Z1_QX1"))
        Zones.Z1_QX2 = convert_to_int(variables.get("Z1_QX2"))
        Zones.Z1_QY1 = convert_to_int(variables.get("Z1_QY1"))
        Zones.Z1_QY2 = convert_to_int(variables.get("Z1_QY2"))

        Zones.Z2_QX1 = convert_to_int(variables.get("Z2_QX1"))
        Zones.Z2_QX2 = convert_to_int(variables.get("Z2_QX2"))
        Zones.Z2_QY1 = convert_to_int(variables.get("Z2_QY1"))
        Zones.Z2_QY2 = convert_to_int(variables.get("Z2_QY2"))

        Zones.Z3_QX1 = convert_to_int(variables.get("Z3_QX1"))
        Zones.Z3_QX2 = convert_to_int(variables.get("Z3_QX2"))
        Zones.Z3_QY1 = convert_to_int(variables.get("Z3_QY1"))
        Zones.Z3_QY2 = convert_to_int(variables.get("Z3_QY2"))

        Zones.Z4_QX1 = convert_to_int(variables.get("Z4_QX1"))
        Zones.Z4_QX2 = convert_to_int(variables.get("Z4_QX2"))
        Zones.Z4_QY1 = convert_to_int(variables.get("Z4_QY1"))
        Zones.Z4_QY2 = convert_to_int(variables.get("Z4_QY2"))

        Zones.Z5_QX1 = convert_to_int(variables.get("Z5_QX1"))
        Zones.Z5_QX2 = convert_to_int(variables.get("Z5_QX2"))
        Zones.Z5_QY1 = convert_to_int(variables.get("Z5_QY1"))
        Zones.Z5_QY2 = convert_to_int(variables.get("Z5_QY2"))

        Zones.Z6_QX1 = convert_to_int(variables.get("Z6_QX1"))
        Zones.Z6_QX2 = convert_to_int(variables.get("Z6_QX2"))
        Zones.Z6_QY1 = convert_to_int(variables.get("Z6_QY1"))
        Zones.Z6_QY2 = convert_to_int(variables.get("Z6_QY2"))

        Zones.Z7_QX1 = convert_to_int(variables.get("Z7_QX1"))
        Zones.Z7_QX2 = convert_to_int(variables.get("Z7_QX2"))
        Zones.Z7_QY1 = convert_to_int(variables.get("Z7_QY1"))
        Zones.Z7_QY2 = convert_to_int(variables.get("Z7_QY2"))

        Zones.Z8_QX1 = convert_to_int(variables.get("Z8_QX1"))
        Zones.Z8_QX2 = convert_to_int(variables.get("Z8_QX2"))
        Zones.Z8_QY1 = convert_to_int(variables.get("Z8_QY1"))
        Zones.Z8_QY2 = convert_to_int(variables.get("Z8_QY2"))

        Zones.Z9_QX1 = convert_to_int(variables.get("Z9_QX1"))
        Zones.Z9_QX2 = convert_to_int(variables.get("Z9_QX2"))
        Zones.Z9_QY1 = convert_to_int(variables.get("Z9_QY1"))
        Zones.Z9_QY2 = convert_to_int(variables.get("Z9_QY2"))

        Zones.Z10_QX1 = convert_to_int(variables.get("Z10_QX1"))
        Zones.Z10_QX2 = convert_to_int(variables.get("Z10_QX2"))
        Zones.Z10_QY1 = convert_to_int(variables.get("Z10_QY1"))
        Zones.Z10_QY2 = convert_to_int(variables.get("Z10_QY2"))

        Zones.Z11_QX1 = convert_to_int(variables.get("Z11_QX1"))
        Zones.Z11_QX2 = convert_to_int(variables.get("Z11_QX2"))
        Zones.Z11_QY1 = convert_to_int(variables.get("Z11_QY1"))
        Zones.Z11_QY2 = convert_to_int(variables.get("Z11_QY2"))

        Zones.Z12_QX1 = convert_to_int(variables.get("Z12_QX1"))
        Zones.Z12_QX2 = convert_to_int(variables.get("Z12_QX2"))
        Zones.Z12_QY1 = convert_to_int(variables.get("Z12_QY1"))
        Zones.Z12_QY2 = convert_to_int(variables.get("Z12_QY2"))

        #Dual Zones ROI Coordinates
        Zones.DZROI_QX1 = convert_to_int(variables.get("DZROI_QX1"))
        Zones.DZROI_QX2 = convert_to_int(variables.get("DZROI_QX2"))
        Zones.DZROI_QY1 = convert_to_int(variables.get("DZROI_QY1"))
        Zones.DZROI_QY2 = convert_to_int(variables.get("DZROI_QY2"))

        #Novel Object Recognition ROI Coordinates (Close Proximity)
        NOR.R1_QX1 = convert_to_int(variables.get("R1_QX1"))
        NOR.R1_QX2 = convert_to_int(variables.get("R1_QX2"))
        NOR.R1_QY1 = convert_to_int(variables.get("R1_QY1"))
        NOR.R1_QY2 = convert_to_int(variables.get("R1_QY2"))

        NOR.R2_QX1 = convert_to_int(variables.get("R2_QX1"))
        NOR.R2_QX2 = convert_to_int(variables.get("R2_QX2"))
        NOR.R2_QY1 = convert_to_int(variables.get("R2_QY1"))
        NOR.R2_QY2 = convert_to_int(variables.get("R2_QY2"))

        #Novel Object Recognition ROI Coordinates (Object Interaction)
        NOR.OBJ1_QX1 = convert_to_int(variables.get("OBJ1_QX1"))
        NOR.OBJ1_QX2 = convert_to_int(variables.get("OBJ1_QX2"))
        NOR.OBJ1_QY1 = convert_to_int(variables.get("OBJ1_QY1"))
        NOR.OBJ1_QY2 = convert_to_int(variables.get("OBJ1_QY2"))

        NOR.OBJ2_QX1 = convert_to_int(variables.get("OBJ2_QX1"))
        NOR.OBJ2_QX2 = convert_to_int(variables.get("OBJ2_QX2"))
        NOR.OBJ2_QY1 = convert_to_int(variables.get("OBJ2_QY1"))
        NOR.OBJ2_QY2 = convert_to_int(variables.get("OBJ2_QY2"))

        #Locomotion Graph ROI Coordinates
        Config.ER_QX1 = variables.get("ER_QX1")
        Config.ER_QX2 = variables.get("ER_QX2")
        Config.ER_QY1 = variables.get("ER_QY1")
        Config.ER_QY2 = variables.get("ER_QY2")


def extractframes():
    codec = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    #If the coordinates were extracted from only one video
    if Config.SingleVideo:


        out = cv2.VideoWriter(str(Config.projectfolder) + '/' + str(Config.sample) + '.mp4', codec, Config.framerate, Config.resolution)

        #this loop if for the cycles described above. RunSess is called inside the loop so that I don't need to set the exact frame each cycle, it only keeps going from where it stopped
        while (Config.cap.isOpened()):
            print('processing frame number: ' + str(Config.cap.get(1)))
            ret, image_np = Config.cap.read()

            if not ret:
                print("No more frames!")

                break

            if Config.CropImage:
                # Crop the frame using the ROI coordinates and append the cropped frame to the list of cropped frames
                roi_frame = image_np[CropImage.y_start:CropImage.y_end, CropImage.x_start:CropImage.x_end]
                if (getsizeof(Config.RawImages) <= 20000):
                    print('appending')
                    Config.RawImages.append(roi_frame)

                else:
                    #LastFrame = (cap.get(1))
                    Config.NoMoreFrames = False
                    Analysis.RunSess(Config.NoMoreFrames, codec, out)

            else:
                if (getsizeof(Config.RawImages) <= 20000):
                    print('appending')
                    Config.RawImages.append(image_np)

                else:
                    # LastFrame = (cap.get(1))
                    Config.NoMoreFrames = False
                    Analysis.RunSess(Config.NoMoreFrames, codec, out)


        #Once there is no more frames, RunSess again with the remaining frames and and set "NoMoreFrames" to True
        Config.NoMoreFrames = True
        Analysis.RunSess(Config.NoMoreFrames, codec, out)

    #if the coordinates were extracted from multiple videos, a txt file was generated and the coordinates are loaded here for each analyzed video
    else:


        for video_name in os.listdir(Config.videopath):
            if video_name.endswith(('.mp4', '.avi')):
                video_path = os.path.join(Config.videopath, video_name)

                Config.cap = cv2.VideoCapture(video_path)
                Config.framerate = round(Config.cap.get(5), 2)
                w = int(Config.cap.get(3))
                h = int(Config.cap.get(4))
                Config.resolution = (w, h)
                ret, Config.image_nl = Config.cap.read()
                Config.img = Config.np.zeros((h, w, 3), dtype=Config.np.uint8)
                Config.img.fill(255)
                Config.video_name = video_name

                out = cv2.VideoWriter(str(Config.projectfolder) + '/' + str(Config.sample) + str(video_name), codec, Config.framerate, Config.resolution)

                ExtractCoordinatestxt(video_name)

                # this loop if for the cycles described above. RunSess is called inside the loop so that I don't need to set the exact frame each cycle, it only keeps going from where it stopped
                while (Config.cap.isOpened()):
                    print('processing frame number: ' + str(Config.cap.get(1)))
                    ret, image_np = Config.cap.read()

                    if not ret:
                        print("No more frames!")

                        break

                    if (getsizeof(Config.RawImages) <= 20000):
                        print('appending')
                        Config.RawImages.append(image_np)

                    else:
                        # LastFrame = (cap.get(1))
                        Config.NoMoreFrames = False
                        Analysis.RunSess(Config.NoMoreFrames, codec, out)

                # Once there is no more frames, RunSess again with the remaining frames and and set "NoMoreFrames" to True
                Config.NoMoreFrames = True
                Analysis.RunSess(Config.NoMoreFrames, codec, out)

            Config.resetvalues()
            #Clear tracked points stored
            for point in Config.TrackedPoints:
                point.clear()
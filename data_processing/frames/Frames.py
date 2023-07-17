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
import ast
import os
import cv2
import numpy as np
from data_processing.frames import Config, Analysis
import GUI
from sys import getsizeof
from coordinates import CropImage, EPM, Locomotion, NOR, Zones

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
        Locomotion.ER_QX1 = convert_to_int(variables.get("ER_QX1"))
        Locomotion.ER_QX2 = convert_to_int(variables.get("ER_QX2"))
        Locomotion.ER_QY1 = convert_to_int(variables.get("ER_QY1"))
        Locomotion.ER_QY2 = convert_to_int(variables.get("ER_QY2"))

        #Crop Image ROI Coordinates
        CropImage.y_start = convert_to_int(variables.get("y_start"))
        CropImage.x_start = convert_to_int(variables.get("x_start"))
        CropImage.y_end = convert_to_int(variables.get("y_end"))
        CropImage.x_end = convert_to_int(variables.get("x_end"))

        #EPM Zones Coordinates
        if Config.EPM:
            #It's not possible to store UMat, so I am saving the Nump Arrays in the txt file, then calling a function that is going to convert into UMAT
            # EPM.polygon_op1 = np.fromstring(variables.get("polygon_op1"))
            # EPM.polygon_op2 = np.fromstring(variables.get("polygon_op2"))
            # EPM.polygon_c1 = np.fromstring(variables.get("polygon_c1"))
            # EPM.polygon_c2 = np.fromstring(variables.get("polygon_c2"))
            # EPM.polygon_center = np.fromstring(variables.get("polygon_center"))

            EPM.p_op1 = ast.literal_eval(variables.get("p_op1"))
            EPM.p_op2 = ast.literal_eval(variables.get("p_op2"))
            EPM.p_c1 = ast.literal_eval(variables.get("p_c1"))
            EPM.p_c2 = ast.literal_eval(variables.get("p_c2"))
            EPM.p_center = ast.literal_eval(variables.get("p_center"))


            #Convert the Nump Array into UMat
            EPM.GenerateUMat()

# The analysis is performed in cycles.
# Typically, TensorFlow is loaded for each frame as a separate session.
# However, this approach is time-consuming due to the overhead of loading a new session for each frame.
# Instead, in the "extractframes" function, a chunk of images is stored in an array, and then a session is loaded only once for the entire array.
# Although this method helps to optimize the loading time, it can lead to memory issues.

# --------------------------
# As the analysis progresses, the tensors start consuming a significant amount of video memory. This can become problematic, even when using multiple GPUs.
# The issue becomes more pronounced when dealing with high-resolution videos or lengthy video footage.
# To mitigate this, we extract the frames in cycles, reducing the frequency of session loading to once every 2k frames or a similar interval.
# You can adjust this number based on the available memory and the desired trade-off between video memory usage and processing time.
# Increasing the interval can save some seconds of processing time if memory is not a constraint.

def extractframes():
    codec = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    # If the coordinates were extracted from only one video
    if Config.SingleVideo:

        out = cv2.VideoWriter(str(Config.projectfolder) + '/' + str(Config.sample) + '.mp4', codec, Config.framerate, Config.resolution)

        # This loop is responsible for implementing the cycles described above.
        # The "RunSess" function is called inside the loop, eliminating the need to specify the exact frame for each cycle.
        # Instead, it continues from where it left off in the previous cycle.
        while (Config.cap.isOpened()):
            print('processing frame number: ' + str(Config.cap.get(1)))
            ret, image_np = Config.cap.read()

            if not ret:
                print("No more frames!")

                break

            if Config.CropImage:
                # Crop the frame using the ROI coordinates and append the cropped frame to the list of cropped frames
                roi_frame = image_np[CropImage.y_start:CropImage.y_end, CropImage.x_start:CropImage.x_end]
                if (getsizeof(Config.RawImages) <= Config.max_frames):
                    print('appending')
                    Config.RawImages.append(roi_frame)

                else:
                    # LastFrame = (cap.get(1))
                    Config.NoMoreFrames = False
                    Analysis.RunSess(Config.NoMoreFrames, codec, out)

            else:
                if (getsizeof(Config.RawImages) <= Config.max_frames):
                    print('appending')
                    Config.RawImages.append(image_np)

                else:
                    # LastFrame = (cap.get(1))
                    Config.NoMoreFrames = False
                    Analysis.RunSess(Config.NoMoreFrames, codec, out)


        # Once all frames have been processed in the cycles, the "RunSess" function is called again with the remaining frames.
        # After this, the variable "NoMoreFrames" is set to True.
        Config.NoMoreFrames = True
        Analysis.RunSess(Config.NoMoreFrames, codec, out)

    # If the coordinates were extracted from multiple videos, a text file containing the coordinates is generated.
    # In this part of the code, the coordinates are loaded for each analyzed video, along with their corresponding video data.
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

                # ----
                # Find the max number of frames per loop
                memory_usage_per_frame = w * h * Config.bytes_per_pixel
                Config.max_frames = int(Config.gpu_memory_bytes / memory_usage_per_frame)

                ExtractCoordinatestxt(video_name)

                if Config.CropImage:
                    # Initialize ROI resolution based on the new resolution (if it was selected)
                    Config.resolution = (CropImage.x_end - CropImage.x_start, CropImage.y_end - CropImage.y_start)

                out = cv2.VideoWriter(str(Config.projectfolder) + '/' + str(Config.sample) + str(video_name), codec, Config.framerate, Config.resolution)

                # This loop is responsible for implementing the cycles described above.
                # The "RunSess" function is called inside the loop, eliminating the need to specify the exact frame for each cycle.
                # Instead, it continues from where it left off in the previous cycle.
                while (Config.cap.isOpened()):
                    print('processing frame number: ' + str(Config.cap.get(1)))
                    ret, image_np = Config.cap.read()

                    if not ret:
                        print("No more frames!")

                        break

                    if Config.CropImage:

                        # This code snippet is responsible for cropping the frame using the ROI (Region of Interest) coordinates and appending the cropped frame to the list of cropped frames.

                        # The ROI coordinates define the region that needs to be extracted from the frame. The frame is then cropped based on these coordinates, resulting in a smaller region of interest.
                        # This can be useful for focusing on specific areas or objects within the frame.

                        # The cropped frame is then added to a list of cropped frames, which can be further processed or analyzed as needed.

                        # Note: Make sure that the ROI coordinates are correctly defined to ensure accurate cropping of the frame. Adjust the coordinates according to your requirements.
                        roi_frame = image_np[CropImage.y_start:CropImage.y_end, CropImage.x_start:CropImage.x_end]

                        # In this part of the code, the resolution is set once again, this time to match the resolution of the ROI frame.
                        #Config.resolution = roi_frame.shape[1], roi_frame.shape[0]
                        #out = cv2.VideoWriter(str(Config.projectfolder) + '/' + str(Config.sample) + str(video_name), codec, Config.framerate, Config.resolution)

                        if (getsizeof(Config.RawImages) <= Config.max_frames):
                            print('appending')
                            Config.RawImages.append(roi_frame)

                        else:
                            # LastFrame = (cap.get(1))
                            Config.NoMoreFrames = False
                            Analysis.RunSess(Config.NoMoreFrames, codec, out)

                    else:

                        if (getsizeof(Config.RawImages) <= Config.max_frames):
                            print('appending')
                            Config.RawImages.append(image_np)

                        else:
                            # LastFrame = (cap.get(1))
                            Config.NoMoreFrames = False
                            Analysis.RunSess(Config.NoMoreFrames, codec, out)

                # After processing all available frames, the code handles any remaining frames that were not processed in previous cycles.

                # The RunSess function is called again with the remaining frames as input to ensure their processing.

                # Once all frames have been processed, the "NoMoreFrames" variable is set to True, indicating that there are no more frames left to process in the video.
                Config.NoMoreFrames = True
                Analysis.RunSess(Config.NoMoreFrames, codec, out)

            Config.resetvalues()
            # Clear the stored tracked points.
            for point in Config.TrackedPoints:
                point.clear()
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
import ctypes
import os
import sys
import types
import cv2
import GUI
from sys import getsizeof
from coordinates import Zones, NOR, Locomotion, CropImage, EPM
from data_processing.frames import Config, Frames, Analysis

module_names = ['coordinates.Locomotion', 'data_processing.frames.Config', 'coordinates.Zones', 'coordinates.NOR', 'coordinates.CropImage', 'coordinates.EPM']

# Function to get screen width using ctypes
def get_screen_width():
    user32 = ctypes.windll.user32
    return user32.GetSystemMetrics(0)

# Reset values from one selection to the other if needed
def reset_values():
    if Config.EPM:
        Config.EPM_Rectangles.clear()

def get_variables_from_module(module):
    module_variables = {}
    for name in dir(module):
        if not name.startswith('__'):
            value = getattr(module, name)
            if not isinstance(value, types.ModuleType):
                module_variables[name] = value
    return module_variables

# Once the coordinates are set in MultiExtraction, this section is responsible for capturing all the relevant global variables, including the coordinates specific to the current video.
# The coordinates are stored in a text file with the same name as the video.
# Afterward, it loops back to MultiExtraction to proceed with zone selection for the next video.
# The stored coordinates will be utilized later during the analysis of each video.
def get_variables_from_modules(video_name):
    variables = {}
    for module_name in module_names:
        if module_name in sys.modules:
            module = sys.modules[module_name]
            module_variables = get_variables_from_module(module)
            variables[module_name] = module_variables

    ApparatusCoordinates = str(Config.projectfolder) + '/' + "info_" + str(video_name) + ".txt"
    with open(ApparatusCoordinates, 'w') as file:
        for module_name, module_variables in variables.items():
            file.write(f"Variables from module '{module_name}':\n")
            for var_name, var_value in module_variables.items():
                file.write(f"{var_name} = {var_value}\n")
            file.write('\n')

# Open the first frame of each video in the folder to allow user-defined zone selection before the actual analysis begins.
# This step enables the user to set the coordinates for the zones on the first frame of each video.
# These coordinates will be utilized during the subsequent analysis.
def MultiExtraction():
    for video_name in os.listdir(Config.videopath):
        if video_name.endswith(('.mp4', '.avi')):
            video_path = os.path.join(Config.videopath, video_name)

            Config.cap = cv2.VideoCapture(video_path)
            Config.framerate = round(Config.cap.get(5), 2)
            w = int(Config.cap.get(3))
            h = int(Config.cap.get(4))
            Config.resolution = (w, h)

            ret, Config.image_nl = Config.cap.read()

            # ----
            # Detect screen width and calculate resize ratio for ROI coordinates extraction on screen
            window_width = get_screen_width()  # Get screen width
            Config.resize_ratio = window_width / w

            # Resize image to fit within the detected window width
            Config.resized_image = cv2.resize(Config.image_nl, (int(w * Config.resize_ratio), int(h * Config.resize_ratio)))

            # ----
            # Find the max number of frames per loop

            # Convert GPU memory to bytes
            gpu_memory_bytes = Config.gpu_memory_gb * 1024 * 1024 * 1024

            bytes_per_pixel = 0.4568  # Average use of memory from the model

            memory_usage_per_frame = w * h * bytes_per_pixel

            Config.max_frames = int(gpu_memory_bytes / memory_usage_per_frame)

            # Create logic to extract the coordinates of each video first
            if Config.CropImage:
                CropImage.CropForAnalysis()

            if Config.EPM:
                EPM.EPM_Selection()

            if Config.TrackZones:
                Zones.SelectZones()

            if Config.DualZone:
                Zones.SelectDualZone()

            if Config.NovelObject:
                NOR.ObjectSelection()

            if Config.Interaction:
                NOR.SpecificObjectSelection()

            if Config.CreateLocomotionGraph:
                Locomotion.CropForLocomotionGraph()

            print('Writing Coordinates into TxT')

            get_variables_from_modules(video_name)

            reset_values()

    print('load model extract frames call')
    Frames.extractframes()
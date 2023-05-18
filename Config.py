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
import numpy as np
import GUI
import Model

global Nosex, Nosey, Headx, Heady, L_Earx, L_Eary, Body1x, Body1y, CenterBodyx, CenterBodyy, Body2x, Body2y, tail1x, tail1y, tail2x, tail2y, tail3x, tail3y, tail4x, tail4y

#Coordinates arrays
#All the tracked points are stored here, if you want to add or delete a point, select that point and remove every part that use the removed array
Nosex = []
Nosey = []
Headx = []
Heady = []
L_Earx = []
L_Eary = []
R_Earx = []
R_Eary = []
Body1x = []
Body1y = []
CenterBodyx = []
CenterBodyy = []
Body2x = []
Body2y = []
tail1x = []
tail1y = []
tail2x = []
tail2y = []
tail3x = []
tail3y = []
tail4x = []
tail4y = []

#Array of the tracked points
TrackedPoints = [Nosex, Nosey, Headx, Heady, L_Earx, L_Eary, R_Earx, R_Eary, Body1x, Body1y, CenterBodyx, CenterBodyy, Body2x, Body2y, tail1x, tail1y, tail2x, tail2y, tail3x, tail3y, tail4x, tail4y]

global Zone1R, Zone2R, Zone3R,Zone4R,Zone5R,Zone6R,Zone7R,Zone8R,Zone9R,Zone10R,Zone11R,Zone12R

#Zones Time
#This is for time in each zone, MABA was built to work till 12 zones, more can be added if you want
# if you are going to use less than 12, don't worry, the code was built to work with 12, but it will work with less than that, at least one zone needs to be selected
Zone1R = 0
Zone2R = 0
Zone3R = 0
Zone3R = 0
Zone4R = 0
Zone5R = 0
Zone6R = 0
Zone7R = 0
Zone8R = 0
Zone9R = 0
Zone10R = 0
Zone11R = 0
Zone12R = 0

global Zone1E, Zone2E, Zone3E, Zone4E, Zone5E, Zone6E, Zone7E, Zone8E, Zone9E, Zone10E, Zone11E, Zone12E
#The number of entries at each zone is also calculated
Zone1E = 0
Zone2E = 0
Zone3E = 0
Zone3E = 0
Zone4E = 0
Zone5E = 0
Zone6E = 0
Zone7E = 0
Zone8E = 0
Zone9E = 0
Zone10E = 0
Zone11E = 0
Zone12E = 0

global InsideZone1, InsideZone2, InsideZone3, InsideZone4, InsideZone5, InsideZone6, InsideZone7, InsideZone8, InsideZone9, InsideZone10, InsideZone11, InsideZone12

InsideZone1 = False
InsideZone2 = False
InsideZone3 = False
InsideZone4 = False
InsideZone5 = False
InsideZone6 = False
InsideZone7 = False
InsideZone8 = False
InsideZone9 = False
InsideZone10 = False
InsideZone11 = False
InsideZone12 = False

global DZR

#Dual Zone Time
DZR = 0

global FirstObjectR, SecondObjectR

#RON Object close proximity time
FirstObjectR = 0
SecondObjectR = 0

global Interaction_FirstObjectR, Interaction_SecondObjectR, I_OBJ_1, I_OBJ_2, N_OBJ_1, N_OBJ_2
#RON interaction with each object
Interaction_FirstObjectR = 0
Interaction_SecondObjectR = 0
I_OBJ_1 = False
I_OBJ_2 = False
N_OBJ_1 = 0
N_OBJ_2 = 0

global image_array, r, r2, font, RawImages, NoMoreFrames
#OpenCV Variables
image_array = []
r = 0
r2 = 0
font = cv2.FONT_HERSHEY_SIMPLEX
RawImages = []
NoMoreFrames = False

global nZones
#number of zones, it is automatically checked after user input
nZones = 0

global TrackZones, NovelObject, CropRon, CreateLocomotionGraph, DualZone, Interaction
#Every function is False by default, the user select what he needs and then run
TrackZones = False
NovelObject = False
CropRon = False
CreateLocomotionGraph = False
DualZone = False
Interaction = False
SingleVideo = False

def resetvalues():
    r = 0

    Interaction_FirstObjectR = 0
    Interaction_SecondObjectR = 0

    FirstObjectR = 0
    SecondObjectR = 0

    DZR = 0

    Zone1R = 0
    Zone2R = 0
    Zone3R = 0
    Zone3R = 0
    Zone4R = 0
    Zone5R = 0
    Zone6R = 0
    Zone7R = 0
    Zone8R = 0
    Zone9R = 0
    Zone10R = 0
    Zone11R = 0
    Zone12R = 0

    Zone1E = 0
    Zone2E = 0
    Zone3E = 0
    Zone3E = 0
    Zone4E = 0
    Zone5E = 0
    Zone6E = 0
    Zone7E = 0
    Zone8E = 0
    Zone9E = 0
    Zone10E = 0
    Zone11E = 0
    Zone12E = 0

#First the remaining variables will be set, using the acquired values by user input
def setglobalvariables(values):
    global modelpath, videopath, projectfolder, sample, cap, framerate, w, h, resolution, image_nl, img, videopath, video_name




    modelpath = values['-ModelPB-']
    videopath = values['-VideoFile-']
    projectfolder = values['-Folder-']
    sample = values['-Sample-']
    cap = cv2.VideoCapture(videopath)
    framerate = round(cap.get(5), 2)
    w = int(cap.get(3))
    h = int(cap.get(4))
    resolution = (w, h)
    ret, image_nl = cap.read()
    img = np.zeros((h, w, 3), dtype=np.uint8)
    img.fill(255)
    video_name = values['-VideoFile-']
    print('Variables set!')

    Model.loadModel()
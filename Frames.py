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
import Config
import GUI
from sys import getsizeof
import Analysis

#The analysis is made in cycles.
#Usually tensorflow is loaded for each frame, as a unique session. I am not using that way because it takes too long to load a new session each time for each frame
#Instead, extractframes stores a chunk of images into a array and then a session is loaded only one time for the entire array.
#Using that method creates a memory problem.
#--------------------------
#Tensors starts to take too much video memory. This can be a problem even with several GPUs.
#This is not a problem if your video has low resolution or if it's not that long, but if you have great resolution and or hours of video, then it would require too much video memory.
#So we extract the frames in cycles, reducing the number of time a session is loaded from each frame to once each 2k frames or something close to that
#You can also increase that number if you have memory enough and want to save a few seconds

def extractframes():
    codec = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    out = cv2.VideoWriter(str(Config.projectfolder) + '/' + str(Config.sample) + '.mp4', codec, Config.framerate, Config.resolution)

    #this loop if for the cycles described above. RunSess is called inside the loop so that I don't need to set the exact frame each cycle, it only keeps going from where it stopped
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
            #LastFrame = (cap.get(1))
            Config.NoMoreFrames = False
            Analysis.RunSess(Config.NoMoreFrames, codec, out)

    #Once there is no more frames, RunSess again with the remaining frames and and set "NoMoreFrames" to True
    Config.NoMoreFrames = True
    Analysis.RunSess(Config.NoMoreFrames, codec, out)
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
from data_processing.frames import Config
from coordinates import Locomotion
from coordinates import Zones
import cv2
from data_processing.frames import Analysis

#Reset values for the next analysis
def ResetValues():
    Config.freezing_frames = 0
    Config.N_Freezing = 0
    Config.freezing_frames_total = 0
    Config.FreezeState = False
    Config.IntervalFreezing = 0
    Config.N_IntervalFreezing = 0
    Config.N_OpenArm = 0
    Config.N_ClosedArm = 0
    Config.N_Center = 0
    Config.N_NoseOutside = 0
    Config.T_NoseOutside = 0
    Config.T_OpenArm = 0
    Config.T_ClosedArm = 0
    Config.T_Center = 0

# Write results into txt file
def writeFile():
    #Take only the video name from the entire path. If it's multiple videos, this variable has already been updated, so it's not going to change here
    if os.path.isabs(Config.video_name):
        Config.video_name = os.path.basename(Config.video_name)

    file_name = str(Config.projectfolder) + '/' + 'Results_' + str(Config.sample) + '_' + str(Config.video_name) + '.txt'
    file = open(file_name, 'w')


    if Config.CreateLocomotionGraph:
        Cutimg = Config.img[Locomotion.ER_QY1: Locomotion.ER_QY2, Locomotion.ER_QX1: Locomotion.ER_QX2]

        cv2.imwrite(str(Config.projectfolder) + '/Locomotion_' + str(Config.sample) + '_' + str(Config.video_name) + '.jpg', Cutimg)
        #cv2.imwrite(str(Config.projectfolder) + '/Locomotion_' + str(Config.sample) + '_' + str(Config.video_name) + '.jpg', Config.img)
        print('Locomotion Graph Created!')

#This entire part can be rebuilt with a loop. However, I tested using this method and the loop,
    # the loading time is basically the same and I think it is better to leave each part exposed so that you can easily modify if there is something
    # different from my analysis to your analysis at specific zone.
    if Config.TrackZones:
        file.write('--- Zones Tracked ---' )
        file.write('\n')
        if Zones.nZones >= 1:
            #here we have ZoneXR (Number of frames with the mice at X Zone) / framerate (number of frames per second) = time of the mice at each zone
            TimeAtZone1 = Config.Zone1R / Config.framerate
            print('Time At Zone 1: ' + str(TimeAtZone1) + ' seconds')
            file.write('Time At Zone 1: ' + str(TimeAtZone1) + ' seconds')
            file.write('\n')
            file.write('Entries in Zone 1: ' + str(Config.Zone1E) + ' time')
            file.write('\n')

            if Zones.nZones >= 2:
                TimeAtZone2 = Config.Zone2R / Config.framerate
                print('Time At Zone 2: ' + str(TimeAtZone2) + ' seconds')
                file.write('Time At Zone 2: ' + str(TimeAtZone2) + ' seconds')
                file.write('\n')
                file.write('Entries in Zone 2: ' + str(Config.Zone2E) + ' time')
                file.write('\n')

                if Zones.nZones >= 3:
                    TimeAtZone3 = Config.Zone3R / Config.framerate
                    print('Time At Zone 3: ' + str(TimeAtZone3) + ' seconds')
                    file.write('Time At Zone 3: ' + str(TimeAtZone3) + ' seconds')
                    file.write('\n')
                    file.write('Entries in Zone 3: ' + str(Config.Zone3E) + ' time')
                    file.write('\n')

                    if Zones.nZones >= 4:
                        TimeAtZone4 = Config.Zone4R / Config.framerate
                        print('Time At Zone 4: ' + str(TimeAtZone4) + ' seconds')
                        file.write('Time At Zone 4: ' + str(TimeAtZone4) + ' seconds')
                        file.write('\n')
                        file.write('Entries in Zone 4: ' + str(Config.Zone4E) + ' time')
                        file.write('\n')

                        if Zones.nZones >= 5:
                            TimeAtZone5 = Config.Zone5R / Config.framerate
                            print('Time At Zone 5: ' + str(TimeAtZone5) + ' seconds')
                            file.write('Time At Zone 5: ' + str(TimeAtZone5) + ' seconds')
                            file.write('\n')
                            file.write('Entries in Zone 5: ' + str(Config.Zone5E) + ' time')
                            file.write('\n')

                            if Zones.nZones >= 6:
                                TimeAtZone6 = Config.Zone6R / Config.framerate
                                print('Time At Zone 6: ' + str(TimeAtZone6) + ' seconds')
                                file.write('Time At Zone 6: ' + str(TimeAtZone6) + ' seconds')
                                file.write('\n')
                                file.write('Entries in Zone 6: ' + str(Config.Zone6E) + ' time')
                                file.write('\n')

                                if Zones.nZones >= 7:
                                    TimeAtZone7 = Config.Zone7R / Config.framerate
                                    print('Time At Zone 7: ' + str(TimeAtZone7) + ' seconds')
                                    file.write('Time At Zone 7: ' + str(TimeAtZone7) + ' seconds')
                                    file.write('\n')
                                    file.write('Entries in Zone 7: ' + str(Config.Zone7E) + ' time')
                                    file.write('\n')

                                    if Zones.nZones >= 8:
                                        TimeAtZone8 = Config.Zone8R / Config.framerate
                                        print('Time At Zone 8: ' + str(TimeAtZone8) + ' seconds')
                                        file.write('Time At Zone 8: ' + str(TimeAtZone8) + ' seconds')
                                        file.write('\n')
                                        file.write('Entries in Zone 8: ' + str(Config.Zone8E) + ' time')
                                        file.write('\n')

                                        if Zones.nZones >= 9:
                                            TimeAtZone9 = Config.Zone9R / Config.framerate
                                            print('Time At Zone 9: ' + str(TimeAtZone9) + ' seconds')
                                            file.write('Time At Zone 9: ' + str(TimeAtZone9) + ' seconds')
                                            file.write('\n')
                                            file.write('Entries in Zone 9: ' + str(Config.Zone9E) + ' time')
                                            file.write('\n')

                                            if Zones.nZones >= 10:
                                                TimeAtZone10 = Config.Zone10R / Config.framerate
                                                print('Time At Zone 10: ' + str(TimeAtZone10) + ' seconds')
                                                file.write('Time At Zone 10: ' + str(TimeAtZone10) + ' seconds')
                                                file.write('\n')
                                                file.write('Entries in Zone 10: ' + str(Config.Zone10E) + ' time')
                                                file.write('\n')

                                                if Zones.nZones >= 11:
                                                    TimeAtZone11 = Config.Zone11R / Config.framerate
                                                    print('Time At Zone 11: ' + str(TimeAtZone11) + ' seconds')
                                                    file.write('Time At Zone 11: ' + str(TimeAtZone11) + ' seconds')
                                                    file.write('\n')
                                                    file.write('Entries in Zone 11: ' + str(Config.Zone11E) + ' time')
                                                    file.write('\n')

                                                    if Zones.nZones >= 12:
                                                        TimeAtZone12 = Config.Zone12R / Config.framerate
                                                        print('Time At Zone 12: ' + str(TimeAtZone12) + ' seconds')
                                                        file.write('Time At Zone 12: ' + str(TimeAtZone12) + ' seconds')
                                                        file.write('\n')
                                                        file.write('Entries in Zone 12: ' + str(Config.Zone12E) + ' time')
                                                        file.write('\n')

    #Dual zone follows the same logic from track zone, but at TimeAtPeriphery, the TimeAtCenter is substracted from the duration of the video
    if Config.DualZone:
        TimeAtCenter = Config.DZR / Config.framerate
        TimeAtPeriphery = (Analysis.r2 / Config.framerate) - TimeAtCenter

        print('Time At Center: ' + str(TimeAtCenter) + ' seconds')
        print('Time At Periphery: ' + str(TimeAtPeriphery) + ' seconds')

        file.write('--- Dual Zone ---')
        file.write('\n')
        file.write('Time At Center: ' + str(TimeAtCenter) + ' seconds')
        file.write('\n')
        file.write('Time At Periphery: ' + str(TimeAtPeriphery) + ' seconds')
        file.write('\n')


    if Config.NovelObject:
        TimeNearFirstObj = Config.FirstObjectR / Config.framerate
        TimeNearSecondObj = Config.SecondObjectR / Config.framerate

        file.write('--- Novel Object Recognition ---')
        file.write('\n')
        file.write('Time Near First Object: ' + str(TimeNearFirstObj) + ' seconds')
        file.write('\n')
        file.write('Time Near Second Object: ' + str(TimeNearSecondObj) + ' seconds')
        file.write('\n')

        if Config.Interaction:
            TimeInteractingFirstObj = Config.Interaction_FirstObjectR / Config.framerate
            TimeInteractingSecondObj = Config.Interaction_SecondObjectR / Config.framerate

            file.write('--- Time Interacting With Objects ---')
            file.write('\n')
            file.write('Time Exploring First Object: ' + str(TimeInteractingFirstObj) + ' seconds')
            file.write('\n')
            file.write('Time Exploring Second Object: ' + str(TimeInteractingSecondObj) + ' seconds')
            file.write('\n')
            file.write('Number of Interactions with First Object: ' + str(Config.N_OBJ_1) + ' time')
            file.write('\n')
            file.write('Number of Interactions with Second Object: ' + str(Config.N_OBJ_2) + ' time')

    if Config.Freeze:
        #Frames total was considered for two points, so it needs to be divided by two
        Config.freezing_frames_total = Config.freezing_frames_total / 2
        #Then, we get the frame rate of the video and divide it again to get the time in seconds
        TimeinFreezeState = Config.freezing_frames_total / Config.framerate
        file.write('--- Freezing State Detection ---')
        file.write('\n')
        file.write('Number of Freezing: ' + str(Config.N_Freezing))
        file.write('\n')
        file.write('Time in Freeze State: ' + str(TimeinFreezeState) + ' seconds')
        file.write('\n')
        file.write('Number of Interval Freezing: ' + str(Config.N_IntervalFreezing))

    if Config.EPM:
        #Calculate the time at each place by dividing the number of frames by the framerate of the video

        TimeinOpenArm = Config.T_OpenArm / Config.framerate
        TimeinClosedArm = Config.T_ClosedArm / Config.framerate
        TimeinCenter = Config.T_Center / Config.framerate
        TimeNoseOutside = Config.T_NoseOutside / Config.framerate

        file.write('--- Elevated Plus Maze ---')
        file.write('\n')
        file.write('Number of Entries at Open Arm: ' + str(Config.N_OpenArm))
        file.write('\n')
        file.write('Number of Entries at Closed Arm: ' + str(Config.N_ClosedArm))
        file.write('\n')
        file.write('Number of Entries at Center: ' + str(Config.N_Center))
        file.write('\n')
        file.write('Number of Times with the Nose Outside: ' + str(Config.N_NoseOutside))
        file.write('\n')
        file.write('Time at Open Arm: ' + str(TimeinOpenArm) + 'seconds')
        file.write('\n')
        file.write('Time at Closed Arm: ' + str(TimeinClosedArm) + 'seconds')
        file.write('\n')
        file.write('Time at Center: ' + str(TimeinCenter) + 'seconds')
        file.write('\n')
        file.write('Time with nose outside: ' + str(TimeNoseOutside) + 'seconds')

    print("File created :", file.name)
    ResetValues()
    file.close
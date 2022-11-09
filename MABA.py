import PySimpleGUI as sg
import numpy
import tensorflow as tf
import cv2
import numpy as np
import sys
import time
from io import StringIO
from sys import getsizeof

"""
    Mice Behavior Tracker

    Tool created for neuroscience analysis that are based on mice

    Copyright 2022 Juarez Culau Batista Pires
"""


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

#Dual Zone Time
DZR = 0

#RON Object close proximity time
FirstObjectR = 0
SecondObjectR = 0

#RON interaction with each object
Interaction_FirstObjectR = 0
Interaction_SecondObjectR = 0
I_OBJ_1 = False
I_OBJ_2 = False
N_OBJ_1 = 0
N_OBJ_2 = 0

#OpenCV Variables
image_array = []
r = 0
r2 = 0
font = cv2.FONT_HERSHEY_SIMPLEX
RawImages = []
NoMoreFrames = False


#number of zones, it is automatically checked after user input
nZones = 0

#Every function is False by default, the user select what he needs and then run
TrackZones = False
NovelObject = False
CropRon = False
CreateLocomotionGraph = False
DualZone = False
Interaction = False

#The GUI (Using PySimpleGUI)
def main():
    global TrackZones, NovelObject, CropRon, CreateLocomotionGraph, DualZone, Interaction
    layout = [[sg.Text('Select the Model PB')],
              [sg.InputText(size=(50, 1), key='-ModelPB-'), sg.FileBrowse()],
              [sg.Text('Select the Video For Analysis')],
              [sg.InputText(size=(50, 1), key='-VideoFile-'), sg.FileBrowse()],
              [sg.Text('Analysis Folder')],
              [sg.InputText(size=(50, 1), key='-Folder-'), sg.FolderBrowse()],
              [sg.Text('Name Your Sample')],
              [sg.InputText(key='-Sample-')],

              [sg.Text('Track Multiple Zones')],
              [sg.Text('Off'),
               sg.Button(image_data=toggle_btn_off, key='-TrackZones?-', button_color=(sg.theme_background_color(), sg.theme_background_color()), border_width=0, metadata=False),
               sg.Text('On')],
              [sg.Text('Dual Zones')],
              [sg.Text('Off'),
               sg.Button(image_data=toggle_btn_off, key='-DualZones-',
                         button_color=(sg.theme_background_color(), sg.theme_background_color()), border_width=0,
                         metadata=False),
               sg.Text('On')],
              [sg.Text('Novel Object Recognition')],
              [sg.Text('Off'),
               sg.Button(image_data=toggle_btn_off, key='-RON?-',
                         button_color=(sg.theme_background_color(), sg.theme_background_color()), border_width=0,
                         metadata=False),
               sg.Text('On')],
              [sg.Text('Crop Object Recognition')],
              [sg.Text('Off'),
               sg.Button(image_data=toggle_btn_off, key='-CropRON?-',
                         button_color=(sg.theme_background_color(), sg.theme_background_color()), border_width=0,
                         metadata=False),
               sg.Text('On')],
              [sg.Text('Detect Interaction Novel Object Recognition')],
              [sg.Text('Off'),
               sg.Button(image_data=toggle_btn_off, key='-Interaction-',
                         button_color=(sg.theme_background_color(), sg.theme_background_color()), border_width=0,
                         metadata=False),
               sg.Text('On')],
              [sg.Text('Locomotion Graph')],
              [sg.Text('Off'),
               sg.Button(image_data=toggle_btn_off, key='-LocomotionGraph?-',
                         button_color=(sg.theme_background_color(), sg.theme_background_color()), border_width=0,
                         metadata=False),
               sg.Text('On')],
              [sg.Button('Run'), sg.Button('Exit')],
              ]

    window = sg.Window('MABA', layout, font='_ 14', finalize=True)

    while True:  # Event Loop
        event, values = window.read()
        #print(window['-TOGGLE-GRAPHIC-'].metadata)
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        #First button logic
        elif event == '-TrackZones?-':  # if the graphical button that changes images
            window['-TrackZones?-'].metadata = not window['-TrackZones?-'].metadata
            window['-TrackZones?-'].update(image_data=toggle_btn_on if window['-TrackZones?-'].metadata else toggle_btn_off)
        if window['-TrackZones?-'].metadata:
            TrackZones = True
        else:
            TrackZones = False

        #Second Button logic
        if event == '-DualZones-':  # if the graphical button that changes images
            window['-DualZones-'].metadata = not window['-DualZones-'].metadata
            window['-DualZones-'].update(image_data=toggle_btn_on if window['-DualZones-'].metadata else toggle_btn_off)
        if window['-DualZones-'].metadata:
            DualZone = True
        else:
            DualZone = False

        #Third Button logic
        if event == '-RON?-':  # if the graphical button that changes images
            window['-RON?-'].metadata = not window['-RON?-'].metadata
            window['-RON?-'].update(image_data=toggle_btn_on if window['-RON?-'].metadata else toggle_btn_off)
        if window['-RON?-'].metadata:
            NovelObject = True
        else:
            NovelObject = False

        # Forth Button logic
        if event == '-CropRON?-':  # if the graphical button that changes images
            window['-CropRON?-'].metadata = not window['-CropRON?-'].metadata
            window['-CropRON?-'].update(image_data=toggle_btn_on if window['-CropRON?-'].metadata else toggle_btn_off)
        if window['-CropRON?-'].metadata:
            CropRon = True
        else:
            CropRon = False

        # Fifth Button logic
        if event == '-Interaction-':  # if the graphical button that changes images
            window['-Interaction-'].metadata = not window['-Interaction-'].metadata
            window['-Interaction-'].update(image_data=toggle_btn_on if window['-Interaction-'].metadata else toggle_btn_off)
        if window['-Interaction-'].metadata:
            Interaction = True
        else:
            Interaction = False

        # Sixth Button logic
        if event == '-LocomotionGraph?-':  # if the graphical button that changes images
            window['-LocomotionGraph?-'].metadata = not window['-LocomotionGraph?-'].metadata
            window['-LocomotionGraph?-'].update(image_data=toggle_btn_on if window['-LocomotionGraph?-'].metadata else toggle_btn_off)
        if window['-LocomotionGraph?-'].metadata:
            CreateLocomotionGraph = True
        else:
            CreateLocomotionGraph = False

        #the process will begin here once "Run" is selected
        if event == 'Run':
            setglobalvariables(values)

    window.close()


#First the remaining variables will be set, using the acquired values by user input
def setglobalvariables(values):
    global modelpath, videopath, projectfolder, sample, cap, framerate, w, h, resolution, image_nl, img
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

    print('Variables set!')

    loadModel()


#Load frozen tensorflow model selected by user
# A default option will be provided, but the recomendation is to train your own model with DeepLabCut and ResNet50.
#However, if your model was not trained with DeepLabCut, a few modifications here will probably be necessary!
def loadModel():
    global input, output, graph
    with tf.io.gfile.GFile(modelpath, "rb") as f:
        graph_def = tf.compat.v1.GraphDef()
        graph_def.ParseFromString(f.read())

    with tf.Graph().as_default() as graph:
        tf.import_graph_def(graph_def, name='')

    # Tensorflow Tensors being used! DO NOT EDIT UNLESS YOU KNOW WHAT YOU ARE DOING!

    input = graph.get_tensor_by_name('Placeholder:0')
    output = graph.get_tensor_by_name('concat_1:0')
    print('Model loaded')


#Most of the next functions are optional, selected by the user before pressing "Run"
#For that reason, the order will vary according to what the user selected.
    if TrackZones:
        DefineZones()

    if DualZone:
        CreateDualZone()

    if NovelObject:
        ObjectSelection()

    if CreateLocomotionGraph:
        CropForLocomotionGraph()

    if not TrackZones and not NovelObject and not DualZone and not CreateLocomotionGraph:
        print('load model extract frames call')
        extractframes()

#Define Zones stores the coordinates of the four points from each ROI selected by the user
#Actually, ROI selection with OpenCV only gives one value from the point selected (x,y,w,h).
#But with only that we can acquire the coordinates of the other three points
def DefineZones():
    print('Defining Zone')
    global Z1_QX1, Z1_QX2, Z1_QY1, Z1_QY2
    global Z2_QX1, Z2_QX2, Z2_QY1, Z2_QY2
    global Z3_QX1, Z3_QX2, Z3_QY1, Z3_QY2
    global Z4_QX1, Z4_QX2, Z4_QY1, Z4_QY2
    global Z5_QX1, Z5_QX2, Z5_QY1, Z5_QY2
    global Z6_QX1, Z6_QX2, Z6_QY1, Z6_QY2
    global Z7_QX1, Z7_QX2, Z7_QY1, Z7_QY2
    global Z8_QX1, Z8_QX2, Z8_QY1, Z8_QY2
    global Z9_QX1, Z9_QX2, Z9_QY1, Z9_QY2
    global Z10_QX1, Z10_QX2, Z10_QY1, Z10_QY2
    global Z11_QX1, Z11_QX2, Z11_QY1, Z11_QY2
    global Z12_QX1, Z12_QX2, Z12_QY1, Z12_QY2


    # Zones field
    Zone = cv2.selectROIs("Select Zones with mouse and then press 'Enter', 'Esc' to finish selection", image_nl, False)
    global nZones

    # Small loop only to discover how many zones were selected by the user
    nZones = 0
    for i in Zone:
        nZones = nZones + 1

    #Even though this part is quite long, it will only run as many as the user selected
    #The math is the same for each zone, but I decided to not use a individual function for all the zones so that you can easily acess the individual coordinates
    #for specific experiments.
    # Zone1
    if nZones >= 1:
        Z1_X2 = ((Zone[0])[0]) + ((Zone[0])[2])
        Z1_Y2 = ((Zone[0])[1]) + ((Zone[0])[3])

        # Z is for zone, first number means which zone it is and the second number mean's which coordinate from the zone, there are four in total for each zone
        #ZX_1 is given by the default function, so there is two items with two individual sections (X, Y, W, H). By acessing X and Y you already have the first coordinate

        Z1_1 = ((Zone[0])[0]), ((Zone[0])[1])

        #
        Z1_2 = Z1_X2, Z1_Y2
        Z1_3 = ((Zone[0])[0]), Z1_Y2
        Z1_4 = Z1_X2, ((Zone[0])[1])

        # Variables for zone calculation
        # Those four are used to know the borders of the selected zone, 1 is for the beginning and 2 for the end
        #QX1 is the X coordinate already given by ROI selection
        Z1_QX1 = ((Zone[0])[0])

        #QX2 = X + W
        Z1_QX2 = Z1_X2

        #Same as with QX1, QY1 is the Y coordinate already given by ROI selection
        Z1_QY1 = ((Zone[0])[1])

        #QY2 = Y + H
        Z1_QY2 = Z1_Y2



        # Zone2
        if nZones >= 2:
            Z2_X2 = ((Zone[1])[0]) + ((Zone[1])[2])
            Z2_Y2 = ((Zone[1])[1]) + ((Zone[1])[3])

            Z2_1 = ((Zone[1])[0]), ((Zone[1])[1])
            Z2_2 = Z2_X2, Z2_Y2
            Z2_3 = ((Zone[1])[0]), Z2_Y2
            Z2_4 = Z2_X2, ((Zone[1])[1])

            # Variables for zone calculation
            Z2_QX1 = ((Zone[1])[0])
            Z2_QX2 = Z2_X2
            Z2_QY1 = ((Zone[1])[1])
            Z2_QY2 = Z2_Y2



            # Zone3
            if nZones >= 3:
                Z3_X2 = ((Zone[2])[0]) + ((Zone[2])[2])
                Z3_Y2 = ((Zone[2])[1]) + ((Zone[2])[3])

                Z3_1 = ((Zone[2])[0]), ((Zone[2])[1])
                Z3_2 = Z3_X2, Z3_Y2
                Z3_3 = ((Zone[2])[0]), Z3_Y2
                Z3_4 = Z3_X2, ((Zone[2])[1])

                # Variables for zone calculation
                Z3_QX1 = ((Zone[2])[0])
                Z3_QX2 = Z3_X2
                Z3_QY1 = ((Zone[2])[1])
                Z3_QY2 = Z3_Y2



                # Zone 4
                if nZones >= 4:
                    Z4_X2 = ((Zone[3])[0]) + ((Zone[3])[2])
                    Z4_Y2 = ((Zone[3])[1]) + ((Zone[3])[3])

                    Z4_1 = ((Zone[3])[0]), ((Zone[3])[1])
                    Z4_2 = Z4_X2, Z4_Y2
                    Z4_3 = ((Zone[3])[0]), Z4_Y2
                    Z4_4 = Z4_X2, ((Zone[3])[1])

                    # Variables for zone calculation
                    Z4_QX1 = ((Zone[3])[0])
                    Z4_QX2 = Z4_X2
                    Z4_QY1 = ((Zone[3])[1])
                    Z4_QY2 = Z4_Y2


                    # Zone 5
                    if nZones >= 5:
                        Z5_X2 = ((Zone[4])[0]) + ((Zone[4])[2])
                        Z5_Y2 = ((Zone[4])[1]) + ((Zone[4])[3])

                        Z5_1 = ((Zone[4])[0]), ((Zone[4])[1])
                        Z5_2 = Z5_X2, Z5_Y2
                        Z5_3 = ((Zone[4])[0]), Z5_Y2
                        Z5_4 = Z5_X2, ((Zone[4])[1])

                        # Variables for zone calculation
                        Z5_QX1 = ((Zone[4])[0])
                        Z5_QX2 = Z5_X2
                        Z5_QY1 = ((Zone[4])[1])
                        Z5_QY2 = Z5_Y2

                        # Zone 6
                        if nZones >= 6:
                            Z6_X2 = ((Zone[5])[0]) + ((Zone[5])[2])
                            Z6_Y2 = ((Zone[5])[1]) + ((Zone[5])[3])

                            Z6_1 = ((Zone[5])[0]), ((Zone[5])[1])
                            Z6_2 = Z6_X2, Z6_Y2
                            Z6_3 = ((Zone[5])[0]), Z6_Y2
                            Z6_4 = Z6_X2, ((Zone[5])[1])

                            # Variables for zone calculation
                            Z6_QX1 = ((Zone[5])[0])
                            Z6_QX2 = Z6_X2
                            Z6_QY1 = ((Zone[5])[1])
                            Z6_QY2 = Z6_Y2

                            # Zone7
                            if nZones >= 7:
                                Z7_X2 = ((Zone[6])[0]) + ((Zone[6])[2])
                                Z7_Y2 = ((Zone[6])[1]) + ((Zone[6])[3])

                                Z7_1 = ((Zone[6])[0]), ((Zone[6])[1])
                                Z7_2 = Z7_X2, Z7_Y2
                                Z7_3 = ((Zone[6])[0]), Z7_Y2
                                Z7_4 = Z7_X2, ((Zone[6])[1])

                                # Variables for zone calculation
                                Z7_QX1 = ((Zone[6])[0])
                                Z7_QX2 = Z7_X2
                                Z7_QY1 = ((Zone[6])[1])
                                Z7_QY2 = Z7_Y2

                                # Zone8
                                if nZones >= 8:
                                    Z8_X2 = ((Zone[7])[0]) + ((Zone[7])[2])
                                    Z8_Y2 = ((Zone[7])[1]) + ((Zone[7])[3])

                                    Z8_1 = ((Zone[7])[0]), ((Zone[7])[1])
                                    Z8_2 = Z8_X2, Z8_Y2
                                    Z8_3 = ((Zone[7])[0]), Z8_Y2
                                    Z8_4 = Z8_X2, ((Zone[7])[1])

                                    # Variables for zone calculation
                                    Z8_QX1 = ((Zone[7])[0])
                                    Z8_QX2 = Z8_X2
                                    Z8_QY1 = ((Zone[7])[1])
                                    Z8_QY2 = Z8_Y2

                                    # Zone9
                                    if nZones >= 9:
                                        Z9_X2 = ((Zone[8])[0]) + ((Zone[8])[2])
                                        Z9_Y2 = ((Zone[8])[1]) + ((Zone[8])[3])

                                        Z9_1 = ((Zone[8])[0]), ((Zone[8])[1])
                                        Z9_2 = Z9_X2, Z9_Y2
                                        Z9_3 = ((Zone[8])[0]), Z9_Y2
                                        Z9_4 = Z9_X2, ((Zone[8])[1])

                                        # Variables for zone calculation
                                        Z9_QX1 = ((Zone[8])[0])
                                        Z9_QX2 = Z9_X2
                                        Z9_QY1 = ((Zone[8])[1])
                                        Z9_QY2 = Z9_Y2

                                        # Zone10
                                        if nZones >= 10:
                                            Z10_X2 = ((Zone[9])[0]) + ((Zone[9])[2])
                                            Z10_Y2 = ((Zone[9])[1]) + ((Zone[9])[3])

                                            Z10_1 = ((Zone[9])[0]), ((Zone[9])[1])
                                            Z10_2 = Z10_X2, Z10_Y2
                                            Z10_3 = ((Zone[9])[0]), Z10_Y2
                                            Z10_4 = Z10_X2, ((Zone[9])[1])

                                            # Variables for zone calculation
                                            Z10_QX1 = ((Zone[9])[0])
                                            Z10_QX2 = Z10_X2
                                            Z10_QY1 = ((Zone[9])[1])
                                            Z10_QY2 = Z10_Y2

                                            # Zone11
                                            if nZones >= 11:
                                                Z11_X2 = ((Zone[10])[0]) + ((Zone[10])[2])
                                                Z11_Y2 = ((Zone[10])[1]) + ((Zone[10])[3])

                                                Z11_1 = ((Zone[10])[0]), ((Zone[10])[1])
                                                Z11_2 = Z11_X2, Z11_Y2
                                                Z11_3 = ((Zone[10])[0]), Z11_Y2
                                                Z11_4 = Z11_X2, ((Zone[10])[1])

                                                # Variables for zone calculation
                                                Z11_QX1 = ((Zone[10])[0])
                                                Z11_QX2 = Z11_X2
                                                Z11_QY1 = ((Zone[10])[1])
                                                Z11_QY2 = Z11_Y2

                                                # Zone12
                                                if nZones >= 12:
                                                    Z12_X2 = ((Zone[11])[0]) + ((Zone[11])[2])
                                                    Z12_Y2 = ((Zone[11])[1]) + ((Zone[11])[3])

                                                    Z12_1 = ((Zone[11])[0]), ((Zone[11])[1])
                                                    Z12_2 = Z12_X2, Z12_Y2
                                                    Z12_3 = ((Zone[11])[0]), Z12_Y2
                                                    Z12_4 = Z12_X2, ((Zone[11])[1])

                                                    # Variables for zone calculation
                                                    Z12_QX1 = ((Zone[11])[0])
                                                    Z12_QX2 = Z12_X2
                                                    Z12_QY1 = ((Zone[11])[1])
                                                    Z12_QY2 = Z12_Y2

    if NovelObject:
        ObjectSelection()

    if DualZone:
        CreateDualZone()

    if not NovelObject and not DualZone:
        print('zone extract frames call')
        extractframes()


#this function will track the mice when he is close to the object but it will not determine interaction,
# the specific object selection determine interaction but for that, the model must have precision enough to track the nose of the mice in your video
#I choose the same logic from the trackzones, this time for only two objects, if for some reason there is more objects in your experiment, then expand here!
def ObjectSelection():
    RON = cv2.selectROIs("select the area around the objects", image_nl, False)
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

    if CreateLocomotionGraph:
        CropForLocomotionGraph()

    if Interaction:
        SpecificObjectSelection()

    if not CreateLocomotionGraph and not Interaction:
        print('object selection extract frames call')
        extractframes()

#this function will be used to track the close proximity to the object
#is important to remember that this functio will only work properly if the model has accuracy enough to track the nose of your mice
#That said, test the model in video or train a new pb model, if you have accuracy to track the nose, then use this function.
# The threshold is being set at 0.8, I recommend to use a higher value if you have trained a new model with your own images and with good resolution
#You can also decrease the threshold, but I don't recommend.
def SpecificObjectSelection():
    OBJ = cv2.selectROIs("Select the Objects, press 'Enter' after selecting the first one, 'Esc' After selecting the second", image_nl, False)
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
    extractframes()


#As you can see, the logic here is not that much different, this time is selecting only one ROI.
def CreateDualZone():
    global DZROI_QX1, DZROI_QX2, DZROI_QY1, DZROI_QY2
    dualzoneROI = cv2.selectROI("Select the Center and then press 'Enter'", image_nl, False)
    DZROI_X2 = (dualzoneROI[0]) + (dualzoneROI[2])
    DZROI_Y2 = (dualzoneROI[1]) + (dualzoneROI[3])

    DZR_1 = (dualzoneROI[0]), (dualzoneROI[1])
    DZR_2 = DZROI_X2, DZROI_Y2
    DZR_3 = (dualzoneROI[0]), DZROI_Y2
    DZR_4 = DZROI_X2, (dualzoneROI[1])

    # Variables for zone calculation
    DZROI_QX1 = (dualzoneROI[0])
    DZROI_QX2 = DZROI_X2
    DZROI_QY1 = (dualzoneROI[1])
    DZROI_QY2 = DZROI_Y2

    if NovelObject:
        ObjectSelection()

    if CreateLocomotionGraph:
        CropForLocomotionGraph()


    if not NovelObject and not CreateLocomotionGraph:
        print('dual zone extract frames call')
        extractframes()

#CropForLocomotionGraph creates a image with the entire path of the mice during the video.
#First it takes the resolution from the video to create a white img and here the aparatus is selected for image cut at the end.
def CropForLocomotionGraph():
    global ER_QX1, ER_QX2, ER_QY1, ER_QY2
    ExperimentROI = cv2.selectROI("Select the Entire Are of Your Experiment 'Enter'", image_nl, False)
    ER_X2 = (ExperimentROI[0]) + (ExperimentROI[2])
    ER_Y2 = (ExperimentROI[1]) + (ExperimentROI[3])

    ER_1 = (ExperimentROI[0]), (ExperimentROI[1])
    ER_2 = ER_X2, ER_Y2
    ER_3 = (ExperimentROI[0]), ER_Y2
    ER_4 = ER_X2, (ExperimentROI[1])

    # Variables for zone calculation
    ER_QX1 = (ExperimentROI[0])
    ER_QX2 = ER_X2
    ER_QY1 = (ExperimentROI[1])
    ER_QY2 = ER_Y2

    if Interaction:
        SpecificObjectSelection()

    print('locomotion extract frames call')
    extractframes()

#The analysis is done in cycles.
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
    out = cv2.VideoWriter(str(projectfolder) + '/' + str(sample) + '.mp4', codec, framerate, resolution)

    #this loop if for the cycles described above. RunSess is called inside the loop so that I don't need to set the exact frame each cycle, it only keeps going from where it stopped
    while (cap.isOpened()):
        print('processing frame number: ' + str(cap.get(1)))
        ret, image_np = cap.read()

        if not ret:
            print("No more frames!")

            break

        if (getsizeof(RawImages) <= 20000):
            print('appending')
            RawImages.append(image_np)

        else:
            #LastFrame = (cap.get(1))
            NoMoreFrames = False
            RunSess(NoMoreFrames, codec, out)

    #Once there is no more frames, RunSess again with the remaining frames and and set "NoMoreFrames" to True
    NoMoreFrames = True
    RunSess(NoMoreFrames, codec, out)

#This is where magic happens, every value acquired so far is compiled here for the analysis
def RunSess(NoMoreFrames, codec, out):

    #The model is already loaded, so I only start the session here
    print('Starting Sess')
    with tf.compat.v1.Session(graph=graph) as sess:
        global r, r2
        #r is used in the loop to know what image to take from the array, the content of the arrays is also cleaned at the end of the sess at each cycle
        #Then, r must be defined as 0 once again.
        r = 0
        for i in range(len(RawImages)):
            #the image is loaded here
            trackerSess = sess.run(output, feed_dict={input: [RawImages[0 + r]]})

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
            Threshold = 0.8

            #here we extract the X and Y coordinate from each tracked point. The threshold have no function in this part.
            Nosex.append((trackerSess[0])[1])
            Nosey.append((trackerSess[0])[0])
            Headx.append((trackerSess[1])[1])
            Heady.append((trackerSess[1])[0])
            L_Earx.append((trackerSess[2])[1])
            L_Eary.append((trackerSess[2])[0])
            R_Earx.append((trackerSess[3])[1])
            R_Eary.append((trackerSess[3])[0])
            Body1x.append((trackerSess[4])[1])
            Body1y.append((trackerSess[4])[0])
            CenterBodyx.append((trackerSess[5])[1])
            CenterBodyy.append((trackerSess[5])[0])
            Body2x.append((trackerSess[6])[1])
            Body2y.append((trackerSess[6])[0])
            tail1x.append((trackerSess[7])[1])
            tail1y.append((trackerSess[7])[0])
            tail2x.append((trackerSess[8])[1])
            tail2y.append((trackerSess[8])[0])
            tail3x.append((trackerSess[9])[1])
            tail3y.append((trackerSess[9])[0])
            tail4x.append((trackerSess[10])[1])
            tail4y.append((trackerSess[10])[0])

#Multiple arrays for each body part will story the coordinates from each frame. A easy way to run multiple analysis if you need it.
            FrameNosex = int(Nosex[0 + r2])
            FrameNosey = int(Nosey[0 + r2])
            FrameHeadx = int(Headx[0 + r2])
            FrameHeady = int(Heady[0 + r2])
            FrameL_Earx = int(L_Earx[0 + r2])
            FrameL_Eary = int(L_Eary[0 + r2])
            FrameR_Earx = int(R_Earx[0 + r2])
            FrameR_Eary = int(R_Eary[0 + r2])
            FrameBody1x = int(Body1x[0 + r2])
            FrameBody1y = int(Body1y[0 + r2])
            FrameCenterBodyx = int(CenterBodyx[0 + r2])
            FrameCenterBodyy = int(CenterBodyy[0 + r2])
            FrameBody2x = int(Body2x[0 + r2])
            FrameBody2y = int(Body2y[0 + r2])
            Frametail1x = int(tail1x[0 + r2])
            Frametail1y = int(tail1y[0 + r2])
            Frametail2x = int(tail2x[0 + r2])
            Frametail2y = int(tail2y[0 + r2])
            Frametail3x = int(tail3x[0 + r2])
            Frametail3y = int(tail3y[0 + r2])
            Frametail4x = int(tail4x[0 + r2])
            Frametail4y = int(tail4y[0 + r2])



            #The coordinates X, Y from the CenterBody will be printed in the image, you can print multiple points if you want or just remove this part, it plays no role on the analysis.
            Sx = str('X: ' + str(FrameCenterBodyx))
            Sy = str('Y: ' + str(FrameCenterBodyy))

            #I am only printing the centerBody here, print more if you want or leave the way it is
            print(FrameCenterBodyx, FrameCenterBodyy)

            #first one must use raw image, after that use local variable 'image' to draw a point at each body part marked by the model
            image = cv2.circle(RawImages[0 + r], (FrameCenterBodyx, FrameCenterBodyy), radius=1, color=(0, 0, 255), thickness=2)

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
            cv2.putText(image, Sx, (50, 50), font, 1, (0, 255, 255), 2, cv2.LINE_4)
            cv2.putText(image, Sy, (50, 100), font, 1, (0, 255, 255), 2, cv2.LINE_4)

            global img
            #the variables down here will mark the presence of the mice at each zone in the frame and use it for further calculations
            global Zone1R, Zone2R, Zone3R,Zone4R,Zone5R,Zone6R,Zone7R,Zone8R,Zone9R,Zone10R, Zone11R, Zone12R
            global Zone1E, Zone2E, Zone3E,Zone4E,Zone5E,Zone6E,Zone7E,Zone8E,Zone9E,Zone10E, Zone11E, Zone12E
            global InsideZone1, InsideZone2, InsideZone3, InsideZone4, InsideZone5, InsideZone6, InsideZone7, InsideZone8, InsideZone9, InsideZone10, InsideZone11, InsideZone12

            #Here it will mark the center body at the white img, for the locomotion graph. You can easily changing the point marked on the image here!
            if CreateLocomotionGraph:
                cv2.circle(img, (FrameCenterBodyx, FrameCenterBodyy), radius=1, color=(0, 0, 0), thickness=4)

            #Track zones analysis happens here.
            #ZoneXE will mark the number of frames that the mice is inside each zone and then divide it by the framerate to acquire the time inside each zone.
            if nZones >= 1:
                if (Z1_QX1 <= FrameCenterBodyx <= Z1_QX2) and (Z1_QY1 <= FrameCenterBodyy <= Z1_QY2):
                    cv2.putText(image, 'Mice in Zone 1!!!', (50, 200), font, 1, (0, 255, 255), 2, cv2.LINE_4)
                    Zone1R = Zone1R + 1

                    if not InsideZone1:
                        Zone1E = Zone1E + 1
                        InsideZone1 = True
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

                if nZones >= 2:
                    if (Z2_QX1 <= FrameCenterBodyx <= Z2_QX2) and (Z2_QY1 <= FrameCenterBodyy <= Z2_QY2):
                        cv2.putText(image, 'Mice in Zone 2!!!', (50, 200), font, 1, (0, 255, 255), 2, cv2.LINE_4)
                        Zone2R = Zone2R + 1

                        if not InsideZone2:
                            Zone2E = Zone2E + 1
                            InsideZone1 = False
                            InsideZone2 = True
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

                    if nZones >= 3:
                        if (Z3_QX1 <= FrameCenterBodyx <= Z3_QX2) and (Z3_QY1 <= FrameCenterBodyy <= Z3_QY2):
                            cv2.putText(image, 'Mice in Zone 3!!!', (50, 200), font, 1, (0, 255, 255), 2, cv2.LINE_4)
                            Zone3R = Zone3R + 1

                            if not InsideZone3:
                                Zone3E = Zone3E + 1
                                InsideZone1 = False
                                InsideZone2 = False
                                InsideZone3 = True
                                InsideZone4 = False
                                InsideZone5 = False
                                InsideZone6 = False
                                InsideZone7 = False
                                InsideZone8 = False
                                InsideZone9 = False
                                InsideZone10 = False
                                InsideZone11 = False
                                InsideZone12 = False

                        if nZones >= 4:
                             if (Z4_QX1 <= FrameCenterBodyx <= Z4_QX2) and (Z4_QY1 <= FrameCenterBodyy <= Z4_QY2):
                                cv2.putText(image, 'Mice in Zone 4!!!', (50, 200), font, 1, (0, 255, 255), 2, cv2.LINE_4)
                                Zone4R = Zone4R + 1

                                if not InsideZone4:
                                    Zone4E = Zone4E + 1
                                    InsideZone1 = False
                                    InsideZone2 = False
                                    InsideZone3 = False
                                    InsideZone4 = True
                                    InsideZone5 = False
                                    InsideZone6 = False
                                    InsideZone7 = False
                                    InsideZone8 = False
                                    InsideZone9 = False
                                    InsideZone10 = False
                                    InsideZone11 = False
                                    InsideZone12 = False

                             if nZones >= 5:
                                if (Z5_QX1 <= FrameCenterBodyx <= Z5_QX2) and (Z5_QY1 <= FrameCenterBodyy <= Z5_QY2):
                                    cv2.putText(image, 'Mice in Zone 5!!!', (50, 200), font, 1, (0, 255, 255), 2, cv2.LINE_4)
                                    Zone5R = Zone5R + 1

                                    if not InsideZone5:
                                        Zone5E = Zone5E + 1
                                        InsideZone1 = False
                                        InsideZone2 = False
                                        InsideZone3 = False
                                        InsideZone4 = False
                                        InsideZone5 = True
                                        InsideZone6 = False
                                        InsideZone7 = False
                                        InsideZone8 = False
                                        InsideZone9 = False
                                        InsideZone10 = False
                                        InsideZone11 = False
                                        InsideZone12 = False

                                if nZones >= 6:
                                    if (Z6_QX1 <= FrameCenterBodyx <= Z6_QX2) and (Z6_QY1 <= FrameCenterBodyy <= Z6_QY2):
                                        cv2.putText(image, 'Mice in Zone 6!!!', (50, 200), font, 1, (0, 255, 255), 2, cv2.LINE_4)
                                        Zone6R = Zone6R + 1

                                        if not InsideZone6:
                                            Zone6E = Zone6E + 1
                                            InsideZone1 = False
                                            InsideZone2 = False
                                            InsideZone3 = False
                                            InsideZone4 = False
                                            InsideZone5 = False
                                            InsideZone6 = True
                                            InsideZone7 = False
                                            InsideZone8 = False
                                            InsideZone9 = False
                                            InsideZone10 = False
                                            InsideZone11 = False
                                            InsideZone12 = False

                                    if nZones >= 7:
                                        if (Z7_QX1 <= FrameCenterBodyx <= Z7_QX2) and (Z7_QY1 <= FrameCenterBodyy <= Z7_QY2):
                                            cv2.putText(image, 'Mice in Zone 7!!!', (50, 200), font, 1, (0, 255, 255), 2, cv2.LINE_4)
                                            Zone7R = Zone7R + 1

                                            if not InsideZone7:
                                                Zone7E = Zone7E + 1
                                                InsideZone1 = False
                                                InsideZone2 = False
                                                InsideZone3 = False
                                                InsideZone4 = False
                                                InsideZone5 = False
                                                InsideZone6 = False
                                                InsideZone7 = True
                                                InsideZone8 = False
                                                InsideZone9 = False
                                                InsideZone10 = False
                                                InsideZone11 = False
                                                InsideZone12 = False

                                        if nZones >= 8:
                                            if (Z8_QX1 <= FrameCenterBodyx <= Z8_QX2) and (Z8_QY1 <= FrameCenterBodyy <= Z8_QY2):
                                                cv2.putText(image, 'Mice in Zone 8!!!', (50, 200), font, 1, (0, 255, 255), 2, cv2.LINE_4)
                                                Zone8R = Zone8R + 1

                                                if not InsideZone8:
                                                    Zone8E = Zone8E + 1
                                                    InsideZone1 = False
                                                    InsideZone2 = False
                                                    InsideZone3 = False
                                                    InsideZone4 = False
                                                    InsideZone5 = False
                                                    InsideZone6 = False
                                                    InsideZone7 = False
                                                    InsideZone8 = True
                                                    InsideZone9 = False
                                                    InsideZone10 = False
                                                    InsideZone11 = False
                                                    InsideZone12 = False

                                            if nZones >= 9:
                                                if (Z9_QX1 <= FrameCenterBodyx <= Z9_QX2) and (Z9_QY1 <= FrameCenterBodyy <= Z9_QY2):
                                                    cv2.putText(image, 'Mice in Zone 9!!!', (50, 200), font, 1, (0, 255, 255), 2, cv2.LINE_4)
                                                    Zone9R = Zone9R + 1

                                                    if not InsideZone9:
                                                        Zone9E = Zone9E + 1
                                                        InsideZone1 = False
                                                        InsideZone2 = False
                                                        InsideZone3 = False
                                                        InsideZone4 = False
                                                        InsideZone5 = False
                                                        InsideZone6 = False
                                                        InsideZone7 = False
                                                        InsideZone8 = False
                                                        InsideZone9 = True
                                                        InsideZone10 = False
                                                        InsideZone11 = False
                                                        InsideZone12 = False

                                                if nZones >= 10:
                                                    if (Z10_QX1 <= FrameCenterBodyx <= Z10_QX2) and (Z10_QY1 <= FrameCenterBodyy <= Z10_QY2):
                                                        cv2.putText(image, 'Mice in Zone 10!!!', (50, 200), font, 1, (0, 255, 255), 2, cv2.LINE_4)
                                                        Zone10R = Zone10R + 1

                                                        if not InsideZone10:
                                                            Zone10E = Zone10E + 1
                                                            InsideZone1 = False
                                                            InsideZone2 = False
                                                            InsideZone3 = False
                                                            InsideZone4 = False
                                                            InsideZone5 = False
                                                            InsideZone6 = False
                                                            InsideZone7 = False
                                                            InsideZone8 = False
                                                            InsideZone9 = False
                                                            InsideZone10 = True
                                                            InsideZone11 = False
                                                            InsideZone12 = False

                                                    if nZones >= 11:
                                                        if (Z11_QX1 <= FrameCenterBodyx <= Z11_QX2) and (Z11_QY1 <= FrameCenterBodyy <= Z11_QY2):
                                                            cv2.putText(image, 'Mice in Zone 11!!!', (50, 200), font, 1, (0, 255, 255), 2, cv2.LINE_4)
                                                            Zone11R = Zone11R + 1

                                                            if not InsideZone11:
                                                                Zone11E = Zone11E + 1
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
                                                                InsideZone11 = True
                                                                InsideZone12 = False

                                                        if nZones >= 12:
                                                            if (Z12_QX1 <= FrameCenterBodyx <= Z12_QX2) and (Z12_QY1 <= FrameCenterBodyy <= Z12_QY2):
                                                                cv2.putText(image, 'Mice in Zone 12!!!', (50, 200), font, 1, (0, 255, 255), 2, cv2.LINE_4)
                                                                Zone12R = Zone12R + 1

                                                                if not InsideZone12:
                                                                    Zone12E = Zone12E + 1
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
                                                                    InsideZone12 = True

            #Same thing from trackzone, but this time with only one zone, the value from the other one is substracted from the duration of the video.
            global DZR
            if DualZone:
                if (DZROI_QX1 <= FrameCenterBodyx <= DZROI_QX2) and (DZROI_QY1 <= FrameCenterBodyy <= DZROI_QY2):
                    cv2.putText(image, 'Mice at Center!!!', (50, 400), font, 1, (0, 255, 255), 2, cv2.LINE_4)
                    DZR = DZR + 1

                else:
                    cv2.putText(image, 'Mice at Periphery!!!', (50, 400), font, 1, (0, 255, 255), 2, cv2.LINE_4)

            #Analyzing the area around the object
            global FirstObjectR, SecondObjectR, Interaction_FirstObjectR, Interaction_SecondObjectR, N_OBJ_1, N_OBJ_2
            if NovelObject:
                if (R1_QX1 <= FrameCenterBodyx <= R1_QX2) and (R1_QY1 <= FrameCenterBodyy <= R1_QY2):
                    cv2.putText(image, 'Close to object 1!!!', (50, 300), font, 1, (0, 255, 255), 2, cv2.LINE_4)
                    FirstObjectR = FirstObjectR + 1


                if (R2_QX1 <= FrameCenterBodyx <= R2_QX2) and (R2_QY1 <= FrameCenterBodyy <= R2_QY2):
                    cv2.putText(image, 'Close to object 2!!!', (50, 300), font, 1, (0, 255, 255), 2, cv2.LINE_4)
                    SecondObjectR = SecondObjectR + 1

                #if the user is analyzing the area around the object and decide to crop the video only for the moments when the mice is close to the object
                #that way he can decide with his own eyes if the mice is inracting with the object, but with a smaller video
                if CropRon:
                    if (R2_QX1 <= FrameCenterBodyx <= R2_QX2) and (R2_QY1 <= FrameCenterBodyy <= R2_QY2) or (R1_QX1 <= FrameCenterBodyx <= R1_QX2) and (
                            R1_QY1 <= FrameCenterBodyy <= R1_QY2):
                        #if CropRon is selected, then the video is going to write only the frames when the mice is close enough to any object.
                        out.write(image)


                #Analyzing the interaction with the object by nose proximity
                if Interaction:
                    if (OBJ1_QX1 <= FrameNosex <= OBJ1_QX2) and (OBJ1_QY1 <= FrameNosey <= OBJ1_QY2):
                        cv2.putText(image, 'Interacting with object 1!!!', (50, 250), font, 1, (0, 255, 255), 2, cv2.LINE_4)

                        #this one is for the time of interaction with each object
                        Interaction_FirstObjectR = Interaction_FirstObjectR + 1

                        #now this one is for the number of interactions with each object
                        if not I_OBJ_1:
                            I_OBJ_1 = True
                            N_OBJ_1 = N_OBJ_1 + 1

                    if (OBJ2_QX1 <= FrameNosex <= OBJ2_QX2) and (OBJ2_QY1 <= FrameNosey <= OBJ2_QY2):
                        cv2.putText(image, 'Interacting with object 2!!!', (50, 250), font, 1, (0, 255, 255), 2, cv2.LINE_4)
                        Interaction_SecondObjectR = Interaction_SecondObjectR + 1

                        if not I_OBJ_2:
                            I_OBJ_2 = True
                            N_OBJ_2 = N_OBJ_2 + 1

                    if not (OBJ1_QX1 <= FrameNosex <= OBJ1_QX2) and (OBJ1_QY1 <= FrameNosey <= OBJ1_QY2):
                        I_OBJ_1 = False

                    if not (OBJ2_QX1 <= FrameNosex <= OBJ2_QX2) and (OBJ2_QY1 <= FrameNosey <= OBJ2_QY2):
                        I_OBJ_2 = False

            #if CropRon was not selected, then it will write the video at each loop
            if not CropRon:
                out.write(image)

            r = r + 1
            r2 = r2 + 1

        #if there is no more frames, then it will clear the RawImages one last time and call the next function "WriteFile"
        if NoMoreFrames:
            RawImages.clear()
            out.release
            print('Video Created')
            writeFile()

        #If there is more frames, then it will clear the RawImages and go back into the extractframes loop until there is no more frames.
        else:
            RawImages.clear()
            print('clearing array extract frames call')

def writeFile():

    #Write results into txt file
    file_name = str(projectfolder) + '/' + "Results_" + str(sample) + ".txt"
    file = open(file_name, 'w')


    if CreateLocomotionGraph:
        Cutimg = img[ER_QY1: ER_QY2, ER_QX1: ER_QX2]

        cv2.imwrite(str(projectfolder) + '/Locomotion_' + str(sample) + '.jpg', Cutimg)
        print('Locomotion Graph Created!')

#This entire part can be rebuilt with a loop. However, I tested using this method and the loop,
    # the loading time is basically the same and I think it is better to leave each part exposed so that you can easily modify if there is something
    # different from my analysis to your analysis at specific zone.
    if TrackZones:
        file.write('--- Zones Tracked ---' )
        file.write('\n')
        if nZones >= 1:
            #here we have ZoneXR (Number of frames with the mice at X Zone) / framerate (number of frames per second) = time of the mice at each zone
            TimeAtZone1 = Zone1R / framerate
            print('Time At Zone 1: ' + str(TimeAtZone1) + ' seconds')
            file.write('Time At Zone 1: ' + str(TimeAtZone1) + ' seconds')
            file.write('\n')
            file.write('Entries in Zone 1: ' + str(Zone1E) + ' time')
            file.write('\n')

            if nZones >= 2:
                TimeAtZone2 = Zone2R / framerate
                print('Time At Zone 2: ' + str(TimeAtZone2) + ' seconds')
                file.write('Time At Zone 2: ' + str(TimeAtZone2) + ' seconds')
                file.write('\n')
                file.write('Entries in Zone 2: ' + str(Zone2E) + ' time')
                file.write('\n')

                if nZones >= 3:
                    TimeAtZone3 = Zone3R / framerate
                    print('Time At Zone 3: ' + str(TimeAtZone3) + ' seconds')
                    file.write('Time At Zone 3: ' + str(TimeAtZone3) + ' seconds')
                    file.write('\n')
                    file.write('Entries in Zone 3: ' + str(Zone3E) + ' time')
                    file.write('\n')

                    if nZones >= 4:
                        TimeAtZone4 = Zone4R / framerate
                        print('Time At Zone 4: ' + str(TimeAtZone4) + ' seconds')
                        file.write('Time At Zone 4: ' + str(TimeAtZone4) + ' seconds')
                        file.write('\n')
                        file.write('Entries in Zone 4: ' + str(Zone4E) + ' time')
                        file.write('\n')

                        if nZones >= 5:
                            TimeAtZone5 = Zone5R / framerate
                            print('Time At Zone 5: ' + str(TimeAtZone5) + ' seconds')
                            file.write('Time At Zone 5: ' + str(TimeAtZone5) + ' seconds')
                            file.write('\n')
                            file.write('Entries in Zone 5: ' + str(Zone5E) + ' time')
                            file.write('\n')

                            if nZones >= 6:
                                TimeAtZone6 = Zone6R / framerate
                                print('Time At Zone 6: ' + str(TimeAtZone6) + ' seconds')
                                file.write('Time At Zone 6: ' + str(TimeAtZone6) + ' seconds')
                                file.write('\n')
                                file.write('Entries in Zone 6: ' + str(Zone6E) + ' time')
                                file.write('\n')

                                if nZones >= 7:
                                    TimeAtZone7 = Zone7R / framerate
                                    print('Time At Zone 7: ' + str(TimeAtZone7) + ' seconds')
                                    file.write('Time At Zone 7: ' + str(TimeAtZone7) + ' seconds')
                                    file.write('\n')
                                    file.write('Entries in Zone 7: ' + str(Zone7E) + ' time')
                                    file.write('\n')

                                    if nZones >= 8:
                                        TimeAtZone8 = Zone8R / framerate
                                        print('Time At Zone 8: ' + str(TimeAtZone8) + ' seconds')
                                        file.write('Time At Zone 8: ' + str(TimeAtZone8) + ' seconds')
                                        file.write('\n')
                                        file.write('Entries in Zone 8: ' + str(Zone8E) + ' time')
                                        file.write('\n')

                                        if nZones >= 9:
                                            TimeAtZone9 = Zone9R / framerate
                                            print('Time At Zone 9: ' + str(TimeAtZone9) + ' seconds')
                                            file.write('Time At Zone 9: ' + str(TimeAtZone9) + ' seconds')
                                            file.write('\n')
                                            file.write('Entries in Zone 9: ' + str(Zone9E) + ' time')
                                            file.write('\n')

                                            if nZones >= 10:
                                                TimeAtZone10 = Zone10R / framerate
                                                print('Time At Zone 10: ' + str(TimeAtZone10) + ' seconds')
                                                file.write('Time At Zone 10: ' + str(TimeAtZone10) + ' seconds')
                                                file.write('\n')
                                                file.write('Entries in Zone 10: ' + str(Zone10E) + ' time')
                                                file.write('\n')

                                                if nZones >= 11:
                                                    TimeAtZone11 = Zone11R / framerate
                                                    print('Time At Zone 11: ' + str(TimeAtZone11) + ' seconds')
                                                    file.write('Time At Zone 11: ' + str(TimeAtZone11) + ' seconds')
                                                    file.write('\n')
                                                    file.write('Entries in Zone 11: ' + str(Zone11E) + ' time')
                                                    file.write('\n')

                                                    if nZones >= 12:
                                                        TimeAtZone12 = Zone12R / framerate
                                                        print('Time At Zone 12: ' + str(TimeAtZone12) + ' seconds')
                                                        file.write('Time At Zone 12: ' + str(TimeAtZone12) + ' seconds')
                                                        file.write('\n')
                                                        file.write('Entries in Zone 12: ' + str(Zone12E) + ' time')
                                                        file.write('\n')

    #Dual zone follows the same logic from track zone, but at TimeAtPeriphery, the TimeAtCenter is substracted from the duration of the video
    if DualZone:
        TimeAtCenter = DZR / framerate
        TimeAtPeriphery = (r2 / framerate) - TimeAtCenter

        print('Time At Center: ' + str(TimeAtCenter) + ' seconds')
        print('Time At Periphery: ' + str(TimeAtPeriphery) + ' seconds')

        file.write('--- Dual Zone ---')
        file.write('\n')
        file.write('Time At Center: ' + str(TimeAtCenter) + ' seconds')
        file.write('\n')
        file.write('Time At Periphery: ' + str(TimeAtPeriphery) + ' seconds')
        file.write('\n')


    if NovelObject:
        TimeNearFirstObj = FirstObjectR / framerate
        TimeNearSecondObj = SecondObjectR / framerate

        file.write('--- Novel Object Recognition ---')
        file.write('\n')
        file.write('Time Near First Object: ' + str(TimeNearFirstObj) + ' seconds')
        file.write('\n')
        file.write('Time Near Second Object: ' + str(TimeNearSecondObj) + ' seconds')
        file.write('\n')

        if Interaction:
            TimeInteractingFirstObj = Interaction_FirstObjectR / framerate
            TimeInteractingSecondObj = Interaction_SecondObjectR / framerate

            file.write('--- Time Interacting With Objects ---')
            file.write('\n')
            file.write('Time Exploring First Object: ' + str(TimeInteractingFirstObj) + ' seconds')
            file.write('\n')
            file.write('Time Exploring Second Object: ' + str(TimeInteractingSecondObj) + ' seconds')
            file.write('\n')
            file.write('Number of Interactions with First Object: ' + str(N_OBJ_1) + ' time')
            file.write('\n')
            file.write('Number of Interactions with Second Object: ' + str(N_OBJ_2) + ' time')

    print("File created :", file.name)
    file.close

if __name__ == '__main__':
    # The base64 strings for the button images
    toggle_btn_off = b'iVBORw0KGgoAAAANSUhEUgAAACgAAAAoCAYAAACM/rhtAAAABmJLR0QA/wD/AP+gvaeTAAAED0lEQVRYCe1WTWwbRRR+M/vnv9hO7BjHpElMKSlpqBp6gRNHxAFVcKM3qgohQSqoqhQ45YAILUUVDRxAor2VAweohMSBG5ciodJUSVqa/iikaePEP4nj2Ovdnd1l3qqJksZGXscVPaylt7Oe/d6bb9/svO8BeD8vA14GvAx4GXiiM0DqsXv3xBcJU5IO+RXpLQvs5yzTijBmhurh3cyLorBGBVokQG9qVe0HgwiXLowdy9aKsY3g8PA5xYiQEUrsk93JTtjd1x3siIZBkSWQudUK4nZO1w3QuOWXV+HuP/fL85klAJuMCUX7zPj4MW1zvC0Ej4yMp/w++K2rM9b70sHBYCjo34x9bPelsgp/XJksZ7KFuwZjr3732YcL64ttEDw6cq5bVuCvgy/sje7rT0sI8PtkSHSEIRIKgCQKOAUGM6G4VoGlwiqoVd2Za9Vl8u87bGJqpqBqZOj86eEHGNch+M7otwHJNq4NDexJD+59RiCEQG8qzslFgN8ibpvZNsBifgXmFvJg459tiOYmOElzYvr2bbmkD509e1ylGEZk1Y+Ssfan18n1p7vgqVh9cuiDxJPxKPT3dfGXcN4Tp3dsg/27hUQs0qMGpRMYjLz38dcxS7Dm3nztlUAb38p0d4JnLozPGrbFfBFm79c8hA3H2AxcXSvDz7/+XtZE1kMN23hjV7LTRnKBh9/cZnAj94mOCOD32gi2EUw4FIRUMm6LGhyiik86nO5NBdGRpxYH14bbjYfJteN/OKR7UiFZVg5T27QHYu0RBxoONV9W8KQ7QVp0iXdE8fANUGZa0QAvfhhXlkQcmjJZbt631oIBnwKmacYoEJvwiuFgWncWnXAtuVBBEAoVVXWCaQZzxmYuut68b631KmoVBEHMUUrJjQLXRAQVSxUcmrKVHfjWWjC3XOT1FW5QrWpc5IJdQhDKVzOigEqS5dKHMVplnNOqrmsXqUSkn+YzWaHE9RW1FeXL7SKZXBFUrXW6jIV6YTEvMAUu0W/G3kcxPXP5ylQZs4fa6marcWvvZfJu36kuHjlc/nMSuXz+/ejxgqPFpuQ/xVude9eu39Jxu27OLvBGoMjrUN04zrNMbgVmOBZ96iPdPZmYntH5Ls76KuxL9NyoLA/brav7n382emDfHqeooXyhQmARVhSnAwNNMx5bu3V1+habun5nWdXhwJZ2C5mirTesyUR738sv7g88UQ0rEkTDlp+1wwe8Pf0klegUenYlgyg7bby75jUTITs2rhCAXXQ2vwxz84vlB0tZ0wL4NEcLX/04OrrltG1s8aOrHhk51SaK0us+n/K2xexBxljcsm1n6x/Fuv1PCWGiKOaoQCY1Vb9gWPov50+fdEqd21ge3suAlwEvA14G/ucM/AuppqNllLGPKwAAAABJRU5ErkJggg=='
    toggle_btn_on = b'iVBORw0KGgoAAAANSUhEUgAAACgAAAAoCAYAAACM/rhtAAAABmJLR0QA/wD/AP+gvaeTAAAD+UlEQVRYCe1XzW8bVRCffbvrtbP+2NhOD7GzLm1VoZaPhvwDnKBUKlVyqAQ3/gAkDlWgPeVQEUCtEOIP4AaHSI0CqBWCQyXOdQuRaEFOk3g3IMWO46+tvZ+PeZs6apq4ipON1MNafrvreTPzfvub92bGAOEnZCBkIGQgZOClZoDrh25y5pdjruleEiX+A+rCaQo05bpuvJ/+IHJCSJtwpAHA/e269g8W5RbuzF6o7OVjF8D3Pr4tSSkyjcqfptPDMDKSleW4DKIggIAD5Yf+Oo4DNg6jbUBlvWLUNutAwZu1GnDjzrcXzGcX2AHw/emFUV6Sfk0pqcKpEydkKSo9q3tkz91uF5aWlo1Gs/mYc+i7tz4//19vsW2AU9O381TiioVCQcnlRsWeQhD3bJyH1/MiFLICyBHiuzQsD1arDvypW7DR9nzZmq47q2W95prm+I9fXfqXCX2AF2d+GhI98Y8xVX0lnxvl2UQQg0csb78ag3NjEeD8lXZ7pRTgftmCu4864OGzrq+5ZU0rCa3m+NzXlzvoAoB3+M+SyWQuaHBTEzKMq/3BMbgM+FuFCDBd9kK5XI5PJBKqLSev+POTV29lKB8rT0yMD0WjUSYLZLxzNgZvIHODOHuATP72Vwc6nQ4Uiw8MUeBU4nHS5HA6TYMEl02wPRcZBJuv+ya+UCZOIBaLwfCwQi1Mc4QXhA+PjWRkXyOgC1uIhW5Qd8yG2TK7kSweLcRGKKVnMNExWWBDTQsH9qVmtmzjiThQDs4Qz/OUSGTwcLwIQTLW58i+yOjpXDLqn1tgmDzXzRCk9eDenjo9yhvBmlizrB3V5dDrNTuY0A7opdndStqmaQLPC1WCGfShYRgHdLe32UrV3ntiH9LliuNrsToNlD4kruN8v75eafnSgC6Luo2+B3fGKskilj5muV6pNhk2Qqg5v7lZ51nBZhNBjGrbxfI1+La5t2JCzfD8RF1HTBGJXyDzs1MblONulEqPDVYXgwDIfNx91IUVbAbY837GMur+/k/XZ75UWmJ77ou5mfM1/0x7vP1ls9XQdF2z9uNsPzosXPNFA5m0/EX72TBSiqsWzN8z/GZB08pWq9VeEZ+0bjKb7RTD2i1P4u6r+bwypo5tZUumEcDAmuC3W8ezIqSGfE6g/sTd1W5p5bKjaWubrmWd29Fu9TD0GlYlmTx+8tTJoZeqYe2BZC1/JEU+wQR5TVEUPptJy3Fs+Vkzgf8lemqHumP1AnYoMZSwsVEz6o26i/G9Lgitb+ZmLu/YZtshfn5FZDPBCcJFQRQ+8ih9DctOFvdLIKHH6uUQnq9yhFu0bec7znZ+xpAGmuqef5/wd8hAyEDIQMjAETHwP7nQl2WnYk4yAAAAAElFTkSuQmCC'

    main()
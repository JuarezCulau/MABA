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
import Config
import EPM
import GUI
import Frames
import Zones
import NOR
import Locomotion
import MultiSelection
import CropImage


#Load frozen tensorflow model selected by user
# A default option will be provided, but the recomendation is to train your own model with DeepLabCut and ResNet50.
#However, if your model was not trained with DeepLabCut, a few modifications here will probably be necessary!

def loadModel():
    global input, output, graph
    with tf.io.gfile.GFile(Config.modelpath, "rb") as f:
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
    if Config.SingleVideo:
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

        if Config.CreateLocomotionGraph:
            Locomotion.CropForLocomotionGraph()

        if not Config.TrackZones and not Config.NovelObject and not Config.DualZone and not Config.CreateLocomotionGraph:
            print('load model extract frames call')
            Frames.extractframes()

    else:
        #MultiSelection()
        MultiSelection.MultiExtraction()
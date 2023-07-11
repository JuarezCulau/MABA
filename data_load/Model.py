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

import GUI
import tensorflow as tf
from data_load import MultiSelection
from data_processing.frames import Config
from data_processing.frames import Frames
from coordinates import Zones
from coordinates import NOR
from coordinates import Locomotion
from coordinates import EPM
from coordinates import CropImage
from coordinates import Cage


#Load frozen tensorflow model selected by user
# Note: It is highly recommended to train your own model using DeepLabCut and ResNet50 for optimal performance.
# However, if your model was not trained with DeepLabCut, certain modifications in this section might be necessary.

def loadModel():
    """
    Description: This function is responsible for loading a pre-trained TensorFlow model into memory.

    Steps:
    1. The model file specified in `Config.modelpath` is read as a binary file using `tf.io.gfile.GFile`.
    2. The contents of the model file are parsed into a TensorFlow `GraphDef` object named `graph_def`.
    3. A new TensorFlow graph is created using `tf.Graph()`, and it becomes the default graph.
    4. The pre-trained model is imported into the graph using `tf.import_graph_def`.
    5. The input tensor is obtained from the graph using its name ('Placeholder:0').
    6. The output tensor is obtained from the graph using its name ('concat_1:0').

    """
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
    if Config.SingleVideo:
        if Config.Cage:
            Cage.Cage_Selection()

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

        #Yale branch only, using the same function to generate the ROI for the Zscore Map
        if Config.CreateLocomotionGraph or Config.Zscore:
            Locomotion.CropForLocomotionGraph()

        if not Config.TrackZones and not Config.NovelObject and not Config.DualZone and not Config.CreateLocomotionGraph:
            print('load model extract frames call')
            Frames.extractframes()

    else:
        MultiSelection.MultiExtraction()
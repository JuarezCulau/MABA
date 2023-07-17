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
import numpy as np
from data_processing.frames import Config

points = []
rectangles = []

#Draw rectangles, visual output only, to check the selection
def draw_rectangle(image, rect_coordinates):
    # Draw lines to connect the four points and form a rectangle
    cv2.line(image, rect_coordinates[0], rect_coordinates[1], (0, 255, 0), 2)
    cv2.line(image, rect_coordinates[1], rect_coordinates[2], (0, 255, 0), 2)
    cv2.line(image, rect_coordinates[2], rect_coordinates[3], (0, 255, 0), 2)
    cv2.line(image, rect_coordinates[3], rect_coordinates[0], (0, 255, 0), 2)

def draw_all_rectangles(image):
    for rect_coordinates in rectangles:
        draw_rectangle(image, rect_coordinates)

def draw_points(event, x, y, flags, param):
    global points

    if event == cv2.EVENT_LBUTTONDOWN:
        # Check if the click is within a previously placed point
        for i, point in enumerate(points):
            distance = cv2.norm((x, y), point)
            if distance < 10:
                # Modify the coordinates of the selected point
                points[i] = (x, y)
                break
        else:
            # Add a new point to the list
            points.append((x, y))

        # Draw circles at the selected points
        image = Config.resized_image
        image_copy = image.copy()
        for point in points:
            cv2.circle(image_copy, point, 3, (0, 0, 255), -1)

        # If four points are selected, calculate the rectangle coordinates
        if len(points) == 4:
            rect_coordinates = calculate_rectangle_coordinates(points)
            Config.Cage_Rectangles.append(rect_coordinates)
            print(Config.Cage_Rectangles)

            # Clear the points list for the next rectangle
            points.clear()

        cv2.imshow("Image", image_copy)

def calculate_rectangle_coordinates(points):
    return [points[0], points[1], points[2], points[3]]

def SetCoordinates(image, polygons):
    global polygon_obj1_umat, polygon_obj2_umat, polygon_obj3_umat

    obj_1 = []
    obj_2 = []
    obj_3 = []

    for polygon in polygons:
        # Connect the points with lines
        for i in range(len(polygon)):
            start_point = polygon[i]
            end_point = polygon[(i + 1) % len(polygon)]
            cv2.line(image, start_point, end_point, (0, 255, 0), 2)

        # Store the polygon coordinates based on their order
        if polygon == polygons[0]:
            obj_1 = polygon
        elif polygon == polygons[1]:
            obj_2 = polygon
        elif polygon == polygons[2]:
            obj_3 = polygon


    # Show the image with the polygons
    cv2.imshow('Image with Polygons', image)
    cv2.waitKey(0)

    # Convert the polygon vertices to a numpy array
    polygon_obj_1 = np.array(obj_1, dtype=np.int32)
    polygon_obj_2 = np.array(obj_2, dtype=np.int32)
    polygon_obj_3 = np.array(obj_3, dtype=np.int32)

    # Create a cv::UMat object from the numpy array
    polygon_obj1_umat = cv2.UMat(polygon_obj_1)
    polygon_obj2_umat = cv2.UMat(polygon_obj_2)
    polygon_obj3_umat = cv2.UMat(polygon_obj_3)

#Only for debug
def draw_polygons(image, polygons):
        for polygon in polygons:
            # Connect the points with lines
            for i in range(len(polygon)):
                start_point = tuple(polygon[i])
                end_point = tuple(polygon[(i + 1) % len(polygon)])
                cv2.line(image, start_point, end_point, (0, 255, 0), 2)  # Customize color and thickness as needed

        # Show the image with the polygons
        cv2.imshow('Image with Polygons', image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

def Cage_Selection():
    # Read the image
    image = Config.resized_image

    # Create a copy of the image for drawing rectangles
    image_copy = image.copy()

    # Create a window and set the mouse callback
    cv2.namedWindow("Image")
    cv2.setMouseCallback("Image", draw_points)

    exit_flag = False  # Flag variable to control the while loop

    while not exit_flag:
        # Show the image with all rectangles
        draw_all_rectangles(image_copy)
        cv2.imshow("Image", image_copy)

        key = cv2.waitKey(1) & 0xFF

        # Press 'r' to reset the points and rectangles
        if key == ord("r"):
            points.clear()
            rectangles.clear()
            image_copy = image.copy()

        # Press 'q' to exit
        if key == ord("q"):
            break

        if key == 27:  # 27 is the ASCII code for the Esc key
            SetCoordinates(Config.resized_image, Config.Cage_Rectangles)
            exit_flag = True  # Set the flag to exit the while loop

    cv2.destroyAllWindows()
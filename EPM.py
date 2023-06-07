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
#C:/Users/juare/Desktop/hangar/MABA/Testing Zone/test.png

import cv2
import numpy as np

import Config

points = []
rectangles = []

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
        image = Config.image_nl
        image_copy = image.copy()
        for point in points:
            cv2.circle(image_copy, point, 3, (0, 0, 255), -1)

        # If four points are selected, calculate the rectangle coordinates
        if len(points) == 4:
            rect_coordinates = calculate_rectangle_coordinates(points)
            Config.EPM_Rectangles.append(rect_coordinates)
            print(Config.EPM_Rectangles)

            # Clear the points list for the next rectangle
            points.clear()

        cv2.imshow("Image", image_copy)

def calculate_rectangle_coordinates(points):
    return [points[0], points[1], points[2], points[3]]

#The whole class is for SetCoordinates5
class Rectangle:
    def __init__(self, coordinates):
        self.coordinates = coordinates
        self.min_x = min(coordinates[0][0], coordinates[1][0], coordinates[2][0], coordinates[3][0])
        self.max_x = max(coordinates[0][0], coordinates[1][0], coordinates[2][0], coordinates[3][0])
        self.min_y = min(coordinates[0][1], coordinates[1][1], coordinates[2][1], coordinates[3][1])
        self.max_y = max(coordinates[0][1], coordinates[1][1], coordinates[2][1], coordinates[3][1])

    def intersects(self, other):
        return not (self.max_x < other.min_x or other.max_x < self.min_x or
                    self.max_y < other.min_y or other.max_y < self.min_y)

    def intersection(self, other):
        x1 = max(self.min_x, other.min_x)
        y1 = max(self.min_y, other.min_y)
        x2 = min(self.max_x, other.max_x)
        y2 = min(self.max_y, other.max_y)
        return [(x1, y1), (x2, y1), (x2, y2), (x1, y2)]

    def adjust_coordinates(self, coordinates):
        for i in range(4):
            self.coordinates[i] = coordinates[i]
        self.min_x = min(coordinates[0][0], coordinates[1][0], coordinates[2][0], coordinates[3][0])
        self.max_x = max(coordinates[0][0], coordinates[1][0], coordinates[2][0], coordinates[3][0])
        self.min_y = min(coordinates[0][1], coordinates[1][1], coordinates[2][1], coordinates[3][1])
        self.max_y = max(coordinates[0][1], coordinates[1][1], coordinates[2][1], coordinates[3][1])

def check_intersection(rectangles):
    intersected_rectangles = []
    for i in range(len(rectangles)):
        for j in range(i+1, len(rectangles)):
            if rectangles[i].intersects(rectangles[j]):
                intersected_rectangles.append((i, j))
    return intersected_rectangles

def remove_intersections(rectangles, intersected_rectangles):
    for pair in intersected_rectangles:
        rect1 = rectangles[pair[0]]
        rect2 = rectangles[pair[1]]
        intersection_coords = rect1.intersection(rect2)
        rect1.adjust_coordinates(intersection_coords)
        rect2.adjust_coordinates(intersection_coords)

def SetCoordinates5():
    # Initialize empty rectangles list
    rectangles = []

    # Create Rectangle objects for each set of coordinates
    for coords in Config.EPM_Rectangles:
        rectangle = Rectangle(coords)
        rectangles.append(rectangle)

    # Check for intersected rectangles
    intersected_rectangles = check_intersection(rectangles)

    # Remove intersections and adjust coordinates
    while intersected_rectangles:
        remove_intersections(rectangles, intersected_rectangles)
        intersected_rectangles = check_intersection(rectangles)

    # Draw rectangles on the image
    image_with_rectangles = np.copy(Config.image_nl)
    for rectangle in rectangles:
        for i in range(4):
            cv2.line(image_with_rectangles, rectangle.coordinates[i], rectangle.coordinates[(i + 1) % 4], (0, 255, 0),
                     2)
        print(rectangle.coordinates)

    # Update Config.image_nl with the image containing the drawn rectangles
    Config.image_nl = image_with_rectangles

    # Display the image with updated rectangles
    cv2.imshow("Updated Rectangles", Config.image_nl)
    cv2.waitKey(0)

def SetCoordinates4():
    rectangles = Config.EPM_Rectangles

    # Calculate the adjusted boundaries for each rectangle
    for i, rect in enumerate(rectangles):
        # Extract the coordinates of the rectangle's corners
        x1, y1 = rect[0]
        x2, y2 = rect[1]
        x3, y3 = rect[2]
        x4, y4 = rect[3]

        # Calculate the bounding box of the rectangle
        min_x = min(x1, x2, x3, x4)
        max_x = max(x1, x2, x3, x4)
        min_y = min(y1, y2, y3, y4)
        max_y = max(y1, y2, y3, y4)

        for j, other_rect in enumerate(rectangles):
            if i != j:
                # Extract the coordinates of the other rectangle's corners
                other_x1, other_y1 = other_rect[0]
                other_x2, other_y2 = other_rect[1]
                other_x3, other_y3 = other_rect[2]
                other_x4, other_y4 = other_rect[3]

                # Calculate the bounding box of the other rectangle
                other_min_x = min(other_x1, other_x2, other_x3, other_x4)
                other_max_x = max(other_x1, other_x2, other_x3, other_x4)
                other_min_y = min(other_y1, other_y2, other_y3, other_y4)
                other_max_y = max(other_y1, other_y2, other_y3, other_y4)

                # Check if the rectangles intersect
                if (
                        min_x <= other_max_x and max_x >= other_min_x and
                        min_y <= other_max_y and max_y >= other_min_y
                ):
                    # Calculate the adjustment values
                    adjustment_x = max(min_x, other_min_x)
                    adjustment_y = max(min_y, other_min_y)

                    # Adjust the coordinates of the current rectangle
                    x1 += adjustment_x - min_x
                    x2 += adjustment_x - min_x
                    x3 += adjustment_x - min_x
                    x4 += adjustment_x - min_x

                    y1 += adjustment_y - min_y
                    y2 += adjustment_y - min_y
                    y3 += adjustment_y - min_y
                    y4 += adjustment_y - min_y

        # Update the coordinates of the current rectangle
        rectangles[i] = [
            (x1, y1),
            (x2, y2),
            (x3, y3),
            (x4, y4)
        ]

        # Draw the updated rectangle on the image
        cv2.rectangle(
            Config.image_nl,
            (int(min_x), int(min_y)),
            (int(max_x), int(max_y)),
            (0, 255, 0),
            2
        )

    # Display the image with updated rectangles
    cv2.imshow("Updated Rectangles", Config.image_nl)
    cv2.waitKey(0)

#Not sure, not working I right now, but may have some use later on
def SetCoordinates2():
    global op1_min_x, op1_max_x, op1_min_y, op1_max_y, op2_min_x, op2_max_x, op2_min_y, op2_max_y, c1_min_x, c1_max_x, c1_min_y, c1_max_y, c2_min_x, c2_max_x, c2_min_y, c2_max_y, center_min_x, center_max_x, center_min_y, center_max_y
    rectangles = Config.EPM_Rectangles
    # Calculate the adjusted boundaries for each rectangle
    for i, rect in enumerate(rectangles):
        # Extract the coordinates of the rectangle's corners
        x1, y1 = rect[0]
        x2, y2 = rect[1]
        x3, y3 = rect[2]
        x4, y4 = rect[3]

        # Initialize the adjusted coordinates with the original values
        adjusted_x1, adjusted_y1 = x1, y1
        adjusted_x2, adjusted_y2 = x2, y2
        adjusted_x3, adjusted_y3 = x3, y3
        adjusted_x4, adjusted_y4 = x4, y4

        for j, other_rect in enumerate(rectangles):
            if i != j:
                # Extract the coordinates of the other rectangle's corners
                other_x1, other_y1 = other_rect[0]
                other_x2, other_y2 = other_rect[1]
                other_x3, other_y3 = other_rect[2]
                other_x4, other_y4 = other_rect[3]

                # Check if the rectangles intersect
                if (
                        x1 <= other_x2 and x2 >= other_x1 and
                        y1 <= other_y2 and y2 >= other_y1 and
                        x3 <= other_x4 and x4 >= other_x3 and
                        y3 <= other_y4 and y4 >= other_y3
                ):
                    # Adjust the overlapping coordinates
                    adjusted_x1 = max(x1, other_x1)
                    adjusted_y1 = max(y1, other_y1)
                    adjusted_x2 = min(x2, other_x2)
                    adjusted_y2 = max(y2, other_y2)
                    adjusted_x3 = max(x3, other_x3)
                    adjusted_y3 = min(y3, other_y3)
                    adjusted_x4 = min(x4, other_x4)
                    adjusted_y4 = min(y4, other_y4)

        # Assign the adjusted coordinates to the corresponding variables
        if i == 0:
            op1_min_x, op1_max_x = min(adjusted_x1, adjusted_x2), max(adjusted_x1, adjusted_x2)
            op1_min_y, op1_max_y = min(adjusted_y1, adjusted_y3), max(adjusted_y1, adjusted_y3)
        elif i == 1:
            op2_min_x, op2_max_x = min(adjusted_x1, adjusted_x2), max(adjusted_x1, adjusted_x2)
            op2_min_y, op2_max_y = min(adjusted_y1, adjusted_y3), max(adjusted_y1, adjusted_y3)
        elif i == 2:
            c1_min_x, c1_max_x = min(adjusted_x1, adjusted_x2), max(adjusted_x1, adjusted_x2)
            c1_min_y, c1_max_y = min(adjusted_y1, adjusted_y3), max(adjusted_y1, adjusted_y3)
        elif i == 3:
            c2_min_x, c2_max_x = min(adjusted_x1, adjusted_x2), max(adjusted_x1, adjusted_x2)
            c2_min_y, c2_max_y = min(adjusted_y1, adjusted_y3), max(adjusted_y1, adjusted_y3)
        elif i == 4:
            center_min_x, center_max_x = min(adjusted_x1, adjusted_x2), max(adjusted_x1, adjusted_x2)
            center_min_y, center_max_y = min(adjusted_y1, adjusted_y3), max(adjusted_y1, adjusted_y3)

        # Draw the updated rectangle on the image
        cv2.rectangle(Config.image_nl, (int(min(adjusted_x1, adjusted_x2)), int(min(adjusted_y1, adjusted_y3))), (int(max(adjusted_x1, adjusted_x2)), int(max(adjusted_y1, adjusted_y3))), (0, 255, 0), 2)

    # Display the image with updated rectangles
    cv2.imshow("Updated Rectangles", Config.image_nl)
    cv2.waitKey(0)

def SetCoordinates3():
    global op1_min_x, op1_max_x, op1_min_y, op1_max_y, op2_min_x, op2_max_x, op2_min_y, op2_max_y, c1_min_x, c1_max_x, c1_min_y, c1_max_y, c2_min_x, c2_max_x, c2_min_y, c2_max_y, center_min_x, center_max_x, center_min_y, center_max_y
    rectangles = Config.EPM_Rectangles

    # Calculate the adjusted boundaries for each rectangle
    for i, rect in enumerate(rectangles):
        # Extract the coordinates of the rectangle's corners
        x1, y1 = rect[0]
        x2, y2 = rect[1]
        x3, y3 = rect[2]
        x4, y4 = rect[3]

        # Adjust the boundaries to avoid intersections
        min_x = min(x1, x2, x3, x4)
        max_x = max(x1, x2, x3, x4)
        min_y = min(y1, y2, y3, y4)
        max_y = max(y1, y2, y3, y4)

        for j, other_rect in enumerate(rectangles):
            if i != j:
                # Check if the rectangles intersect
                other_min_x = min(other_rect[0][0], other_rect[1][0], other_rect[2][0], other_rect[3][0])
                other_max_x = max(other_rect[0][0], other_rect[1][0], other_rect[2][0], other_rect[3][0])
                other_min_y = min(other_rect[0][1], other_rect[1][1], other_rect[2][1], other_rect[3][1])
                other_max_y = max(other_rect[0][1], other_rect[1][1], other_rect[2][1], other_rect[3][1])

                if min_x <= other_max_x and max_x >= other_min_x and min_y <= other_max_y and max_y >= other_min_y:
                    # Adjust the boundaries by taking the average value
                    min_x = (min_x + other_max_x) / 2
                    max_x = (max_x + other_min_x) / 2
                    min_y = (min_y + other_max_y) / 2
                    max_y = (max_y + other_min_y) / 2

                    print(min_x, max_x, min_y, max_y)
                    print("3409834039")

        # Assign the adjusted boundaries to the corresponding variables
        if i == 0:
            op1_min_x = min_x
            op1_max_x = max_x
            op1_min_y = min_y
            op1_max_y = max_y
        elif i == 1:
            op2_min_x = min_x
            op2_max_x = max_x
            op2_min_y = min_y
            op2_max_y = max_y
        elif i == 2:
            c1_min_x = min_x
            c1_max_x = max_x
            c1_min_y = min_y
            c1_max_y = max_y
        elif i == 3:
            c2_min_x = min_x
            c2_max_x = max_x
            c2_min_y = min_y
            c2_max_y = max_y
        elif i == 4:
            center_min_x = min_x
            center_max_x = max_x
            center_min_y = min_y
            center_max_y = max_y

#This function is going to be called in the case of multiple videos, to set the UMat from tne NumpArray saved on the txt file
def GenerateUMat():
    # Create a cv::UMat object from the numpy array
    polygon_op1_umat = cv2.UMat(polygon_op1)
    polygon_op2_umat = cv2.UMat(polygon_op2)
    polygon_c1_umat = cv2.UMat(polygon_c1)
    polygon_c2_umat = cv2.UMat(polygon_c2)
    polygon_center_umat = cv2.UMat(polygon_center)

def SetCoordinates6(image, polygons):
    global polygon_op1_umat, polygon_op2_umat, polygon_c1_umat, polygon_c2_umat, polygon_center_umat
    global polygon_op1, polygon_op2, polygon_c1, polygon_c2, polygon_center

    p_op1 = []
    p_op2 = []
    p_c1 = []
    p_c2 = []
    p_center = []

    for polygon in polygons:
        # Connect the points with lines
        for i in range(len(polygon)):
            start_point = polygon[i]
            end_point = polygon[(i + 1) % len(polygon)]
            cv2.line(image, start_point, end_point, (0, 255, 0), 2)  # Customize color and thickness as needed

        # Store the polygon coordinates based on their order
        if polygon == polygons[0]:
            p_op1 = polygon
        elif polygon == polygons[1]:
            p_op2 = polygon
        elif polygon == polygons[2]:
            p_c1 = polygon
        elif polygon == polygons[3]:
            p_c2 = polygon
        elif polygon == polygons[4]:
            p_center = polygon

    # Show the image with the polygons
    cv2.imshow('Image with Polygons', image)
    cv2.waitKey(0)

    # Convert the polygon vertices to a numpy array
    polygon_op1 = np.array(p_op1, dtype=np.int32)
    polygon_op2 = np.array(p_op2, dtype=np.int32)
    polygon_c1 = np.array(p_c1, dtype=np.int32)
    polygon_c2 = np.array(p_c2, dtype=np.int32)
    polygon_center = np.array(p_center, dtype=np.int32)

    # Create a cv::UMat object from the numpy array
    polygon_op1_umat = cv2.UMat(polygon_op1)
    polygon_op2_umat = cv2.UMat(polygon_op2)
    polygon_c1_umat = cv2.UMat(polygon_c1)
    polygon_c2_umat = cv2.UMat(polygon_c2)
    polygon_center_umat = cv2.UMat(polygon_center)

#Only for debug, at least for now
def draw_polygons(image, polygons):
        for polygon in polygons:
            # Connect the points with lines
            for i in range(len(polygon)):
                start_point = polygon[i]
                end_point = polygon[(i + 1) % len(polygon)]
                cv2.line(image, start_point, end_point, (0, 255, 0), 2)  # Customize color and thickness as needed

        # Show the image with the polygons
        cv2.imshow('Image with Polygons', image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


def SetCoordinates():
    global op1_min_x, op1_max_x, op1_min_y, op1_max_y, op2_min_x, op2_max_x, op2_min_y, op2_max_y, c1_min_x, c1_max_x, c1_min_y, c1_max_y, c2_min_x, c2_max_x, c2_min_y, c2_max_y, center_min_x, center_max_x, center_min_y, center_max_y
    #Open Arm 1
    # Extract the coordinates of the rectangle's corners
    x1, y1 = (Config.EPM_Rectangles[0])[0]
    x2, y2 = (Config.EPM_Rectangles[0])[1]
    x3, y3 = (Config.EPM_Rectangles[0])[2]
    x4, y4 = (Config.EPM_Rectangles[0])[3]

    # Calculate the bounding box of the rectangle
    op1_min_x = min(x1, x2, x3, x4)
    op1_max_x = max(x1, x2, x3, x4)
    op1_min_y = min(y1, y2, y3, y4)
    op1_max_y = max(y1, y2, y3, y4)

    #Open Arm 2
    #Repeat for the other rectangles selected
    # Extract the coordinates of the rectangle's corners
    x1, y1 = (Config.EPM_Rectangles[1])[0]
    x2, y2 = (Config.EPM_Rectangles[1])[1]
    x3, y3 = (Config.EPM_Rectangles[1])[2]
    x4, y4 = (Config.EPM_Rectangles[1])[3]

    # Calculate the bounding box of the rectangle
    op2_min_x = min(x1, x2, x3, x4)
    op2_max_x = max(x1, x2, x3, x4)
    op2_min_y = min(y1, y2, y3, y4)
    op2_max_y = max(y1, y2, y3, y4)

    #Closed Arm 1
    # Extract the coordinates of the rectangle's corners
    x1, y1 = (Config.EPM_Rectangles[2])[0]
    x2, y2 = (Config.EPM_Rectangles[2])[1]
    x3, y3 = (Config.EPM_Rectangles[2])[2]
    x4, y4 = (Config.EPM_Rectangles[2])[3]

    # Calculate the bounding box of the rectangle
    c1_min_x = min(x1, x2, x3, x4)
    c1_max_x = max(x1, x2, x3, x4)
    c1_min_y = min(y1, y2, y3, y4)
    c1_max_y = max(y1, y2, y3, y4)

    #Closed Arm 2
    # Extract the coordinates of the rectangle's corners
    x1, y1 = (Config.EPM_Rectangles[3])[0]
    x2, y2 = (Config.EPM_Rectangles[3])[1]
    x3, y3 = (Config.EPM_Rectangles[3])[2]
    x4, y4 = (Config.EPM_Rectangles[3])[3]

    # Calculate the bounding box of the rectangle
    c2_min_x = min(x1, x2, x3, x4)
    c2_max_x = max(x1, x2, x3, x4)
    c2_min_y = min(y1, y2, y3, y4)
    c2_max_y = max(y1, y2, y3, y4)

    #Center
    # Extract the coordinates of the rectangle's corners
    x1, y1 = (Config.EPM_Rectangles[4])[0]
    x2, y2 = (Config.EPM_Rectangles[4])[1]
    x3, y3 = (Config.EPM_Rectangles[4])[2]
    x4, y4 = (Config.EPM_Rectangles[4])[3]

    # Calculate the bounding box of the rectangle
    center_min_x = min(x1, x2, x3, x4)
    center_max_x = max(x1, x2, x3, x4)
    center_min_y = min(y1, y2, y3, y4)
    center_max_y = max(y1, y2, y3, y4)

    #SetCoordinates6(Config.image_nl, Config.EPM_Rectangles)

def EPM_Selection():
    # Read the image
    image = Config.image_nl

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
            SetCoordinates6(Config.image_nl, Config.EPM_Rectangles)
            #RemoveIntersections()
            #SetCoordinates5()
            exit_flag = True  # Set the flag to exit the while loop

    cv2.destroyAllWindows()
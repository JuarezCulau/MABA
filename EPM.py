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
            SetCoordinates()
            exit_flag = True  # Set the flag to exit the while loop

    cv2.destroyAllWindows()
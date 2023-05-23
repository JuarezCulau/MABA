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
        image_copy = image.copy()
        for point in points:
            cv2.circle(image_copy, point, 3, (0, 0, 255), -1)

        # If four points are selected, calculate the rectangle coordinates
        if len(points) == 4:
            rect_coordinates = calculate_rectangle_coordinates(points)
            rectangles.append(rect_coordinates)
            print(rectangles)

            # Clear the points list for the next rectangle
            points.clear()

        cv2.imshow("Image", image_copy)

def calculate_rectangle_coordinates(points):
    return [points[0], points[1], points[2], points[3]]

# Read the image
image = cv2.imread("C:/Users/juare/Desktop/hangar/MABA/Testing Zone/test.png")

# Create a copy of the image for drawing rectangles
image_copy = image.copy()

# Create a window and set the mouse callback
cv2.namedWindow("Image")
cv2.setMouseCallback("Image", draw_points)

while True:
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

cv2.destroyAllWindows()
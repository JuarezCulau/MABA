import numpy as np
import cv2
from shapely.geometry import Polygon

class Rectangle:
    def __init__(self, coordinates):
        self.coordinates = coordinates

    def intersects(self, other):
        self_polygon = Polygon(self.coordinates)
        other_polygon = Polygon(other.coordinates)
        return self_polygon.intersects(other_polygon)

    def intersection(self, other):
        self_polygon = Polygon(self.coordinates)
        other_polygon = Polygon(other.coordinates)
        intersection_polygon = self_polygon.intersection(other_polygon)
        return list(intersection_polygon.exterior.coords)

    def adjust_coordinates(self, coordinates):
        self.coordinates = coordinates

def check_intersection(rectangles):
    intersected_rectangles = []
    for i in range(len(rectangles)):
        for j in range(i+1, len(rectangles)):
            if rectangles[i].intersects(rectangles[j]):
                intersected_rectangles.append((i, j))
    return intersected_rectangles

def find_nearest_point(point, points):
    distances = np.linalg.norm(np.array(points) - np.array(point), axis=1)
    nearest_idx = np.argmin(distances)
    return points[nearest_idx]

def remove_intersections(rectangles, intersected_rectangles):
    for rect_idx, (i, j) in enumerate(intersected_rectangles):
        rect1 = rectangles[i]
        rect2 = rectangles[j]
        intersection_coords = rect1.intersection(rect2)

        nearest_point1 = find_nearest_point(intersection_coords[0], rect1.coordinates)
        nearest_point2 = find_nearest_point(intersection_coords[1], rect1.coordinates)

        midpoint1 = [(nearest_point1[0] + rect1.coordinates[0][0]) / 2, (nearest_point1[1] + rect1.coordinates[0][1]) / 2]
        midpoint2 = [(nearest_point2[0] + rect1.coordinates[1][0]) / 2, (nearest_point2[1] + rect1.coordinates[1][1]) / 2]

        cv2.circle(image, (nearest_point1), 5, (0, 255, 0), 2)
        cv2.circle(image, (nearest_point2), 5, (0, 255, 0), 2)

        cv2.circle(image, (int(intersection_coords[0][0]), int(intersection_coords[0][1])), 5, (0, 255, 0), 2)
        cv2.circle(image, (int(intersection_coords[1][0]), int(intersection_coords[1][1])), 5, (0, 255, 0), 2)


        cv2.circle(image, (int(midpoint1[0]), int(midpoint1[1])), 5, (0, 255, 0), 2)
        cv2.circle(image, (int(midpoint2[0]), int(midpoint2[1])), 5, (0, 255, 0), 2)
        cv2.imshow("nearest point", image)
        cv2.waitKey(0)

        print("caubanga")
        print(rect1.coordinates)
        print(intersection_coords)
#here is the problem, the intersection_coords is detecting the zone of intersection but I should calculate what new coordinates to pass over here

        # Adjust coordinates individually
        rect1.adjust_coordinates(intersection_coords)
        rect2.adjust_coordinates(intersection_coords)

def draw_rectangles(image, rectangles):
    image_with_rectangles = image.copy()
    for rect in rectangles:
        pts = [list(point) for point in rect.coordinates]
        pts = np.array(pts, np.int32)
        cv2.polylines(image_with_rectangles, [pts], True, (0, 255, 0), 2)
    return image_with_rectangles

# Load the image
videopath = ("C:/Users/juare/Desktop/hangar/MABA/Testing Zone/EPM Videos/G1-1_Trim.mp4")
cap = cv2.VideoCapture(videopath)
ret, image = cap.read()

# Create the rectangles
coordinates = [[(495, 693), (531, 776), (825, 658), (792, 584)],
               [(1192, 419), (1238, 488), (1450, 402), (1415, 324)],
               [(834, 303), (723, 28), (840, 8), (950, 272)],
               [(911, 510), (961, 624), (1060, 582), (1019, 482)],
               [(939, 577), (1123, 1024), (1246, 977), (1041, 548)]]

rectangles = [Rectangle(coords) for coords in coordinates]

# Check for intersections
intersected_rectangles = check_intersection(rectangles)

# Remove intersections and adjust coordinates
remove_intersections(rectangles, intersected_rectangles)

# Draw rectangles on the image
image_with_rectangles = draw_rectangles(image, rectangles)

# Display the image with rectangles
cv2.imshow("Image with Rectangles", image_with_rectangles)
cv2.waitKey(0)
cv2.destroyAllWindows()
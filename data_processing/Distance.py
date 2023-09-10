import math


class DistanceTracker:
    def __init__(self):
        self.total_movement = 0  # Initialize total movement as zero
        self.prev_point = None  # Initialize the previous point as None

    def calculate_euclidean_difference(self, current_point):
        if self.prev_point is None:
            # If there's no previous point, set it and return 0 as the initial movement
            self.prev_point = current_point
            return 0

        # Calculate Euclidean distance between current and previous points
        euclidean_distance = math.sqrt(
            (current_point[0] - self.prev_point[0]) ** 2 +
            (current_point[1] - self.prev_point[1]) ** 2
        )

        # Update total movement
        self.total_movement += euclidean_distance

        # Update the previous point
        self.prev_point = current_point

        return euclidean_distance



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


# Example usage:
if __name__ == "__main__":
    tracker = DistanceTracker()

    # Simulate processing video frames
    for frame_number in range(1, 11):
        # Replace these coordinates with the actual coordinates of the mouse point in the frame
        current_mouse_point = (frame_number * 10, frame_number * 10)

        # Calculate and get the Euclidean difference
        euclidean_difference = tracker.calculate_euclidean_difference(current_mouse_point)

        # Print the results for each frame
        print(
            f"Frame {frame_number}: Euclidean Difference = {euclidean_difference}, Total Movement = {tracker.total_movement}")



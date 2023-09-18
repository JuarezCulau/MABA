def detect_bursts(total_distance, total_frames_processed, burst_threshold, frames_to_check):
    if total_frames_processed < frames_to_check:
        # Insufficient frames processed to check for bursts
        return False

    # Calculate the average velocity over the last 'frames_to_check' frames
    average_velocity = total_distance / total_frames_processed

    # Check if the average velocity exceeds the burst threshold
    if average_velocity > burst_threshold:
        return True  # Burst detected
    else:
        return False  # No burst detected

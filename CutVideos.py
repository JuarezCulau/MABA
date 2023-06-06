import os
import cv2


def create_duration_folders(output_folder):
    durations = ['2min', '2_5min', '8_33min', '13_58min', '19_41min', '25_25min']
    for duration in durations:
        folder_path = os.path.join(output_folder, duration)
        os.makedirs(folder_path, exist_ok=True)


def cut_videos_in_folder(folder_path):
    output_folder = os.path.join(folder_path, 'cut_videos')
    create_duration_folders(output_folder)

    for file_name in os.listdir(folder_path):
        if file_name.endswith('.mp4'):
            video_path = os.path.join(folder_path, file_name)
            video_name = os.path.splitext(file_name)[0]

            output_paths = [
                os.path.join(output_folder, '2min', f'{video_name}_2min.mp4'),
                os.path.join(output_folder, '2_5min', f'{video_name}_2_5min.mp4'),
                os.path.join(output_folder, '3_08min', f'{video_name}_3_08min.mp4'),
                os.path.join(output_folder, '3_66min', f'{video_name}_3_66min.mp4'),
                os.path.join(output_folder, '4_25min', f'{video_name}_4_25min.mp4'),
                os.path.join(output_folder, '4_83min', f'{video_name}_4_83min.mp4')
            ]

            time_intervals = [(0, 120), (120, 150), (155, 185), (190, 220), (225, 255), (260, 290)]

            cut_video(video_path, output_paths, time_intervals)


def cut_video(video_path, output_paths, time_intervals):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)

    for i in range(len(time_intervals)):
        start_frame = int(time_intervals[i][0] * fps)
        end_frame = int(time_intervals[i][1] * fps)
        duration_folder = os.path.dirname(output_paths[i])
        os.makedirs(duration_folder, exist_ok=True)

        cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

        writer = cv2.VideoWriter(output_paths[i], cv2.VideoWriter_fourcc(*'mp4v'), fps,
                                 (int(cap.get(3)), int(cap.get(4))))

        while cap.isOpened() and cap.get(cv2.CAP_PROP_POS_FRAMES) < end_frame:
            ret, frame = cap.read()
            if not ret:
                break
            writer.write(frame)

        writer.release()

    cap.release()


# Usage
folder_path = 'C:/Users/juare/Desktop/hangar/MABA/Odaias Analysis/Edited Videos/Videos/Ext_3567y56'
cut_videos_in_folder(folder_path)
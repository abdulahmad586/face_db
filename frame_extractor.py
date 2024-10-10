import cv2
import os

def extract_frames(video_path, output_folder, num_frames):
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Open the video file
    cap = cv2.VideoCapture(video_path)

    # Get the total number of frames in the video
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Calculate the interval at which frames will be extracted
    frame_interval = total_frames // num_frames

    extracted_count = 0
    frame_number = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Extract the frame at the calculated interval
        if frame_number % frame_interval == 0:
            frame_filename = os.path.join(output_folder, f'frame_{extracted_count}.jpg')
            cv2.imwrite(frame_filename, frame)
            print(f'Extracted frame {extracted_count} at position {frame_number}')
            extracted_count += 1

        frame_number += 1

        # Stop if we've extracted enough frames
        if extracted_count >= num_frames:
            break

    cap.release()
    print(f'Extracted {extracted_count} frames from {video_path}.')


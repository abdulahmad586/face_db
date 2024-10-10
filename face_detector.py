import os
from ultralytics import YOLO
import cv2

model = YOLO('models/yolov8s_face_silu.pt')

def detect_faces_in_dir(frames_dir_path):
    #sd
    files = os.listdir(frames_dir_path)
    detected_faces = []
    for image_file in files:
        image = cv2.imread(os.path.join(frames_dir_path, image_file))
        results = model(image)
        if len(results) > 0:
            detections = results[0]
            # Loop through the detected faces
            for i, (xyxy, confidence, class_id) in enumerate(zip(detections.boxes.xyxy, detections.boxes.conf, detections.boxes.cls)):
                # Extract the bounding box coordinates
                x1, y1, x2, y2 = map(int, xyxy)  # Convert to integers
                print(f'Face {i+1} detected with confidence {confidence:.2f}')

                # Crop the face from the image using the bounding box
                face_crop = image[y1:y2, x1:x2]
                detected_faces.append(face_crop)
        os.unlink(os.path.join(frames_dir_path, image_file))
    return detected_faces

def detect_faces(image_path):
    detected_faces = []
    image = cv2.imread(image_path)
    results = model(image)
    if len(results) > 0:
        detections = results[0]
        # Loop through the detected faces
        for i, (xyxy, confidence, class_id) in enumerate(zip(detections.boxes.xyxy, detections.boxes.conf, detections.boxes.cls)):
            # Extract the bounding box coordinates
            x1, y1, x2, y2 = map(int, xyxy)  # Convert to integers
            print(f'Face {i+1} detected with confidence {confidence:.2f}')

            # Crop the face from the image using the bounding box
            face_crop = image[y1:y2, x1:x2]
            detected_faces.append(face_crop)
    os.unlink(image_path)
    return detected_faces
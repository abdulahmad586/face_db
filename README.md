# Face Recognition Flask App

This Flask application allows users to register by uploading videos, which are processed to extract face embeddings for face recognition. The app also includes functionality to scan images and identify users based on their face embeddings.

## Features

- **User Registration**: Upload a video, extract frames, detect faces, and store face embeddings.
- **Face Scanning**: Upload an image, detect faces, and match the face to registered users using embeddings.
- **File Handling**: Upload and store images or videos for processing.
- **Face Embeddings**: Use face embeddings to uniquely identify users.

## Requirements

To run this project, you need the following installed:

- Python 3.x
- Flask
- Additional dependencies for face detection, video frame extraction, and face embeddings.

### Install Dependencies

First, set up a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

Then install the required packages:

```bash
pip install -r requirements.txt
```

## File Structure

project-root/
│
├── app.py                # Main Flask application
├── uploads/              # Folder for uploaded files (images, videos)
├── templates/            # HTML templates (register_user.html, scan_image.html)
├── frame_extractor.py    # Logic for extracting frames from videos
├── face_detector.py      # Logic for detecting faces in images
├── face_embeddings.py    # Logic for generating face embeddings
├── app_storage.py        # Storage management for registered users
├── face_scanner.py       # Logic for scanning and identifying face embeddings
├── README.md             # Project documentation
└── requirements.txt      # List of required Python libraries

## How to Run the Application

Clone this repository:

bash
Copy code
git clone https://github.com/yourusername/face-recognition-flask-app.git
cd face-recognition-flask-app
Install the dependencies:

bash
Copy code
pip install -r requirements.txt
Create the necessary directories:

bash
Copy code
mkdir uploads
Start the Flask app:

bash
Copy code
flask run
By default, the application runs on http://127.0.0.1:5000/.

Usage
Registering a User
Navigate to http://127.0.0.1:5000/register-user.
Upload a video file containing the user's face.
The app will extract frames from the video, detect the face, and store the face embeddings for future recognition.
Scanning an Image
Navigate to http://127.0.0.1:5000/scan-image.
Upload an image containing the face of a registered user.
The app will scan the image, detect the face, and attempt to match it with the stored face embeddings. If a match is found, the user’s name will be displayed.
API Endpoints
/register-user (GET/POST)
GET: Displays a form to upload a video for user registration.
POST: Processes the uploaded video, extracts face embeddings, and registers the user.
/scan-image (GET/POST)
GET: Displays a form to upload an image for face scanning.
POST: Processes the uploaded image, extracts face embeddings, and identifies the user if a match is found.
/uploads/<filename>
Downloads a file from the uploads directory.
License
This project is licensed under the MIT License. See the LICENSE file for details.
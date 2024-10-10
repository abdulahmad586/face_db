from flask import Flask, request, send_from_directory, render_template
import os
from frame_extractor import extract_frames
from face_detector import detect_faces_in_dir, detect_faces
from face_embeddings import face_embeddings
from app_storage import new_user, get_user_by_id
from face_scanner import scan_face

app = Flask(__name__)

# Set the upload folder
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Create folder if it doesn't exist

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Define allowed file extensions
ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
ALLOWED_VIDEO_EXTENSIONS = {'mp4'}

def allowed_image(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS

def allowed_video(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_VIDEO_EXTENSIONS

def unique_name(name=""):
    return name.replace(' ','-').lower()

# Route to upload files
@app.route('/register-user', methods=['GET'])
def upload_form():
    return render_template('register_user.html')

@app.route('/register-user', methods=['POST'])
def register_user():
    # Check if the file is part of the request
    if 'file' not in request.files:
        return "No file part"
    
    file = request.files['file']
    form = request.form

    name = form.get('name', default='')
    username = unique_name(name)

    # If the user doesn't select a file, the browser submits an empty file
    if file.filename == '':
        return "No selected file"

    if file and allowed_video(file.filename):
        filename = file.filename
        video_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(video_path)

        #extract picture frames from the video
        frames_dir = f"generated/{username}/frames/"
        extract_frames(video_path=video_path, output_folder=frames_dir, num_frames=10)
        os.unlink(video_path)

        #extract the faces in the frames above
        faces = detect_faces_in_dir(frames_dir)
        embeddings = face_embeddings(faces)
        os.rmdir(frames_dir)
        os.rmdir(f"generated/{username}/")
        new_user(name, username, embeddings)
        return "User added successfully"

@app.route('/scan-image', methods=['GET'])
def scan_face_image():
    return render_template('scan_image.html')

@app.route('/scan-image', methods=['POST'])
def scan_image():
    # Check if the file is part of the request
    if 'file' not in request.files:
        return "No file part"
    
    file = request.files['file']
    # If the user doesn't select a file, the browser submits an empty file
    if file.filename == '':
        return "No selected file"

    if file and allowed_image(file.filename):
        filename = file.filename
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(image_path)

        faces = detect_faces(image_path)
        embeddings = face_embeddings(faces)
        if(len(embeddings) > 0):
            uid = scan_face(embeddings[0])
            if(uid != -1):
                user = get_user_by_id(uid)
                return user[1]
            else:
                return "Unable to determine user"

    return "User not found"

# Route to download files
@app.route('/uploads/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)

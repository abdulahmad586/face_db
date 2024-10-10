import cv2
import numpy as np
from keras_facenet import FaceNet
from sklearn.preprocessing import normalize

embedder = FaceNet()

def face_embeddings(faces):
    embeddings = embedder.embeddings(faces)
    # for face in faces:
        
    #     # Resize face to 160x160 pixels (required input size for FaceNet)
    #     face_image_resized = cv2.resize(face, (160, 160))

    #     # Normalize pixel values between -1 and 1
    #     face_image_normalized = (face_image_resized - 127.5) / 127.5

    #     # Expand dimensions to match FaceNet input
    #     face_image_normalized = np.expand_dims(face_image_normalized, axis=0)

    #     # Generate embeddings using FaceNet
    #     embedding = embedder.embeddings(face)

    #     # Remove extra dimensions to get a 1D array of size (512)
    #     embedding = embedding.reshape(-1)  # shape becomes (512,)
    #     print(embedding[0:10])
    #     embeddings.append(embedding)
        
    # Convert list of 1D arrays into a 2D numpy array
    return embeddings
    result = np.array(embeddings)
    print("RESULT")
    print(result)
    print("END RESULT")
    return result  # shape will be (n, 512) where n is the number of faces


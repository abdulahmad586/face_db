from app_storage import search_neighbors
from sklearn.preprocessing import normalize

def scan_face(face_embedding):
    face_embedding = normalize(face_embedding.reshape(1, -1)).flatten()
        
    results = search_neighbors(face_embedding, k=5)
    print(f"GOTTEN SEARCH RESULTS {results}")
    if(len(results) > 0):
        return results[0][0]
    return -1

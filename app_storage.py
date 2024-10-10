import sqlite3
import numpy as np
import hnswlib
from sklearn.preprocessing import normalize

# Initialize HNSWlib Index
dim = 512  # Embedding dimension
max_elements = 10000  # Set based on your data size
M = 16  # Set M higher to allow for more connections (try values between 16-48)
ef_construction = 200  # Higher value makes construction slower but more accurate

hnsw_index = hnswlib.Index(space='l2', dim=dim)
hnsw_index.init_index(max_elements=max_elements, ef_construction=ef_construction, M=M)

# Store only user metadata in SQLite
conn = sqlite3.connect('storage.db')
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT NOT NULL, username TEXT NOT NULL)')
conn.commit()

def new_user(name: str, username: str, face_embeddings):
    conn = sqlite3.connect('storage.db')
    c = conn.cursor()
    cursor = c.execute('INSERT INTO users (name, username) VALUES (?, ?)', (name, username))
    uid = cursor.lastrowid

    for embedding in face_embeddings:
        # embedding = normalize(embedding.reshape(1, -1)).flatten()
        if embedding.ndim == 1:
            embedding = np.expand_dims(embedding, axis=0)
        # Ensure face_embeddings is a 2D numpy array before adding
        if isinstance(embedding, np.ndarray) and embedding.ndim == 2:
            # Add embeddings to HNSWlib index, associating each with the user's UID
            hnsw_index.add_items(embedding, [uid] * embedding.shape[0])  # Duplicate uid for each embedding
            print(f"Added {embedding.shape[0]} embeddings for user {uid}.")
            # print(embedding[0:10])
        else:
            print("Error: face_embeddings must be a 2D numpy array.")

    conn.commit()
    return uid, name, username


def get_user_by_id(uid: int):
    conn = sqlite3.connect('storage.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE id=?', (uid,))
    row = c.fetchone()
    return row

def get_paginated_embeddings(page: int, page_size: int):
    offset = (page-1) * page_size

    # Get embeddings from HNSWlib for the current page
    all_ids, all_embeddings = hnsw_index.get_ids(), hnsw_index.get_items()  # Retrieve all
    embeddings = [(all_ids[i], all_embeddings[i]) for i in range(offset, offset + page_size)]

    return embeddings

def search_neighbors(embedding: np.ndarray, k: int = 5):
    """
    Search for the top k nearest neighbors for a given embedding.
    
    Parameters:
    embedding (np.ndarray): The query embedding to search for.
    k (int): The number of nearest neighbors to return (default is 5).
    
    Returns:
    List of tuples with the format (user_id, distance).
    """
    # Ensure the input embedding is a 2D array (1 sample with 512 dimensions)

    print("Number of items in the index:", hnsw_index.get_current_count())

    if embedding.ndim == 1:
        embedding = np.expand_dims(embedding, axis=0)

    # Set ef parameter for the search (try different values like 10, 50, 100, etc.)
    hnsw_index.set_ef(100)  # You can adjust this value based on your needs

    # Perform the search for the k-nearest neighbors in the HNSW index
    labels, distances = hnsw_index.knn_query(embedding, k=k)
    
    # Return the results as a list of tuples (user_id, distance)
    results = [(int(labels[0][i]), distances[0][i]) for i in range(len(labels[0]))]
    return results

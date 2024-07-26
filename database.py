import sqlite3
import numpy as np

def create_connection():
    conn = sqlite3.connect('face_embeddings.db')
    return conn

def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS embeddings (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        filename TEXT NOT NULL,
                        embedding BLOB NOT NULL
                      )''')
    conn.commit()
    conn.close()

def add_embedding(filename, embedding):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO embeddings (filename, embedding) VALUES (?, ?)",
                   (filename, embedding.tobytes()))
    conn.commit()
    conn.close()

def get_all_embeddings():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, filename, embedding FROM embeddings")
    rows = cursor.fetchall()
    conn.close()
    return [(row[0], row[1], np.frombuffer(row[2], dtype=np.float64)) for row in rows]

def cosine_similarity(embedding1, embedding2):
    dot_product = np.dot(embedding1, embedding2)
    norm_product = np.linalg.norm(embedding1) * np.linalg.norm(embedding2)
    return dot_product / norm_product

def embedding_exists(new_embedding, threshold=0.3):
    all_embeddings = get_all_embeddings()
    for _, _, embedding in all_embeddings:
        similarity = cosine_similarity(embedding, new_embedding)
        if similarity > threshold:
            return True
    return False

def get_images():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT filename FROM embeddings")
    rows = cursor.fetchall()
    conn.close()
    return [row[0] for row in rows]

# Create the table if it doesn't exist
create_table()

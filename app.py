from flask import Flask, render_template, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import os
import face_recognition
from PIL import Image
from chromadb.utils.embedding_functions import OpenCLIPEmbeddingFunction
from chromadb.utils.data_loaders import ImageLoader
import chromadb
import database as db

# Initialize embedding function and data loader
embedding_function = OpenCLIPEmbeddingFunction()
data_loader = ImageLoader()

# Initialize ChromaDB client and collection
chroma_client = chromadb.PersistentClient(path="chroma_images")
collection = chroma_client.get_or_create_collection(
    name='multimodal_collection',
    embedding_function=embedding_function,
    data_loader=data_loader
)

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
FACE_FOLDER = 'static/faces'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(FACE_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['FACE_FOLDER'] = FACE_FOLDER

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Add file to ChromaDB collection
        collection.add(
            ids=[filename],
            images=[file_path]
        )
        
        # Process face detection
        image = face_recognition.load_image_file(file_path)
        face_locations = face_recognition.face_locations(image)
        face_encodings = face_recognition.face_encodings(image, face_locations)

        face_filenames = []
        for i, (top, right, bottom, left) in enumerate(face_locations):
            face_image = image[top:bottom, left:right]
            pil_image = Image.fromarray(face_image)
            face_filename = f"{os.path.splitext(filename)[0]}_face_{i}.jpg"
            face_path = os.path.join(app.config['FACE_FOLDER'], face_filename)
            pil_image.save(face_path)
            
            face_collection = chroma_client.get_or_create_collection(
                                        name='face_multimodal_collection',
                                        embedding_function=embedding_function,
                                        data_loader=data_loader
                                    )
            face = face_collection.query(
                query_images=[face_path]
            )
            print(face)
            print(face.get('distances'))
            # print(face.get('distances')[0][0])
            distances = face.get('distances')
            ids = face.get('ids')

            if distances[0]:
                distance = distances[0][0]
                if distance <= 0.15:
                    print(f'Skipping face {face_filename} - distance {distance} is below threshold')
                    continue
                else:
                    print(f'Adding face {face_filename} - distance {distance} is above threshold')
                    
                    # Add face to the collection and database
                    face_collection.add(
                        ids=[face_filename],
                        images=[face_path]
                    )
                    db.add_embedding(face_filename, face_encodings[i])
                    face_filenames.append(face_filename)
            else:
                # Add face to the collection if no previous faces are found
                print(f'Adding face {face_filename} - no previous faces found')
                face_collection.add(
                    ids=[face_filename],
                    images=[face_path]
                )
                db.add_embedding(face_filename, face_encodings[i])
                face_filenames.append(face_filename)

        return jsonify({'message': 'File uploaded successfully', 'faces': face_filenames}), 200

@app.route('/search', methods=['POST'])
def search_files():
    query = request.form.get('query')
    if not query:
        return 'No query provided', 400
    
    # Query ChromaDB collection
    results = collection.query(query_texts=[query])
    results = results.get('ids')[0]
    
    # Format results for JSON response
    response = [{'filename': id} for id in results]
    
    return jsonify(response), 200

@app.route('/images', methods=['GET'])
def get_images():
    image_list = os.listdir(app.config['UPLOAD_FOLDER'])
    return jsonify(image_list), 200

@app.route('/faces', methods=['GET'])
def get_faces():
    # Fetch face filenames from SQLite database
    image_list = db.get_images()
    return jsonify(image_list), 200


@app.route('/uploads/<filename>')
def serve_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/faces/<filename>')
def serve_face(filename):
    return send_from_directory(app.config['FACE_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)

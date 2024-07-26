# Skypiea Cloud Storage

**Skypiea** is a cloud storage application that allows users to upload images, detect faces, and manage those images. It includes features for face detection, storing face embeddings, and searching for similar faces.

## Features

- **File Upload:** Upload images to cloud storage.
- **Face Detection:** Detect faces in uploaded images and save face images separately.
- **Face Embeddings:** Store face embeddings in a SQLite database to avoid duplicates.
- **Search Functionality:** Search for images based on face embeddings and display similar results.

## Technologies

- **Backend:** Flask
- **Database:** SQLite for storing face embeddings
- **Face Detection:** `face_recognition` library
- **Embeddings Storage:** ChromaDB
- **Frontend:** HTML, CSS, JavaScript

## Installation

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/yourusername/skypiea.git
    cd skypiea
    ```

2. **Create a Virtual Environment and Activate It:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Setup Database:**

    Create the SQLite database and tables:

    ```bash
    python database.py
    ```

5. **Run the Application:**

    ```bash
    python app.py
    ```

    The application will be accessible at `http://127.0.0.1:5000`.

## Directory Structure

```
skypiea/
│
├── static/
│   ├── uploads/       # Uploaded images
│   └── faces/         # Detected face images
│   └── css/           # css files
│   └── js/            # JavaScript for frontend interactions
│
├── templates/
│   ├── index.html     # Main HTML file
│
├── app.py             # Flask application
├── database.py        # SQLite database management
└── requirements.txt   # Python dependencies
```

## Face Detection and Embeddings

The application uses the `face_recognition` library to detect faces and compute embeddings. Faces are saved as separate images and their embeddings are stored in a SQLite database to manage duplicates and ensure uniqueness.

## Troubleshooting

- **Duplicate Faces:** Ensure that the threshold in the `embedding_exists` function is properly set to avoid duplicates.
- **Missing Files:** Check file paths and ensure that the server has proper access permissions to read/write files.

## Contributing

Feel free to fork the repository and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.
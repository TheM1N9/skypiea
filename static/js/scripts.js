document.getElementById('uploadForm').addEventListener('submit', async function (e) {
    e.preventDefault();
    const formData = new FormData(this);
    const response = await fetch('/upload', {
        method: 'POST',
        body: formData
    });
    const result = await response.json();
    alert(result.message);
    loadUploadedFiles();
    displayDetectedFaces(result.faces || []); // Ensure result.faces is an array
});

document.getElementById('searchForm').addEventListener('submit', async function (e) {
    e.preventDefault();
    const formData = new FormData(this);
    const response = await fetch('/search', {
        method: 'POST',
        body: formData
    });
    const results = await response.json();
    displaySearchResults(results);
});

async function loadUploadedFiles() {
    const response = await fetch('/images');
    const files = await response.json();
    const uploadedFilesDiv = document.getElementById('uploadedFiles');
    uploadedFilesDiv.innerHTML = '';
    files.forEach(file => {
        const img = document.createElement('img');
        img.src = `/uploads/${file}`;
        img.alt = file;
        img.style.width = '100px'; // Adjust size as needed
        uploadedFilesDiv.appendChild(img);
    });
}

async function loadDetectedFaces() {
    const response = await fetch('/faces');
    const faces = await response.json();
    displayDetectedFaces(faces);
}

function displayDetectedFaces(faces) {
    const detectedFacesDiv = document.getElementById('detectedFaces');
    detectedFacesDiv.innerHTML = '';
    faces.forEach(face => {
        const img = document.createElement('img');
        img.src = `/faces/${face}`;
        img.alt = face;
        img.style.width = '100px'; // Adjust size as needed
        img.onclick = () => searchByFace(face);
        detectedFacesDiv.appendChild(img);
    });
}

async function searchByFace(face) {
    const response = await fetch('/search', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: `query=${face}`
    });
    const results = await response.json();
    displaySearchResults(results);
}

function displaySearchResults(results) {
    const searchResultsDiv = document.getElementById('searchResults');
    searchResultsDiv.innerHTML = '';
    results.forEach(result => {
        const img = document.createElement('img');
        img.src = `/uploads/${result.filename}`;
        img.alt = result.filename;
        img.style.width = '100px'; // Adjust size as needed
        searchResultsDiv.appendChild(img);
    });
}

// Load initial data on page load
loadUploadedFiles();
loadDetectedFaces();

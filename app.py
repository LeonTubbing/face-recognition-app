from flask import Flask, render_template, request
import face_recognition
import os  # Add this import to access environment variables

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    file = request.files['file']
    file.save('uploaded_image.jpg')

    uploaded_image = face_recognition.load_image_file('uploaded_image.jpg')
    uploaded_encoding = face_recognition.face_encodings(uploaded_image)[0]

    # Assume you have a folder with reference images
    folder_path = "static/image_library/"
    matches = search_in_library(uploaded_encoding, folder_path)
    return render_template('results.html', matches=matches)

def search_in_library(uploaded_encoding, folder_path):
    matches = []
    for filename in os.listdir(folder_path):
        if filename.endswith((".jpg", ".jpeg", ".png")):
            image_path = os.path.join(folder_path, filename)
            test_image = face_recognition.load_image_file(image_path)
            test_encodings = face_recognition.face_encodings(test_image)
            for test_encoding in test_encodings:
                results = face_recognition.compare_faces([uploaded_encoding], test_encoding)
                if results[0]:
                    matches.append(filename)
    return matches

if __name__ == '__main__':
    # Use the PORT assigned by Heroku or default to 5000 for local development
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
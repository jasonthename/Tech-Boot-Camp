from flask import Flask, request, jsonify, send_from_directory
import whisper
import os
from werkzeug.utils import secure_filename
from flask_cors import CORS

app = Flask(__name__, static_folder="frontend")
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

model = whisper.load_model("tiny")

@app.route("/")
def serve_index():
    return send_from_directory("frontend", "index.html")

@app.route("/transcribe", methods=["POST"])
def transcribe_audio():
    if "audio" not in request.files:
        return jsonify({"error": "No audio file provided"}), 400

    file = request.files["audio"]
    filename = secure_filename(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)

    try:
        result = model.transcribe(file_path, language="English", fp16=False)
        return jsonify({"text": result["text"]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        os.remove(file_path)

if __name__ == "__main__":
    app.run(debug=True)

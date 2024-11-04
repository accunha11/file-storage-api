from flask import Flask, request, jsonify, send_file
from auth import auth
from uuid import uuid4
import os
import json

app = Flask(__name__)

# File upload settings
UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {".pdf", ".jpg", ".jpeg", ".png"}

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# Load and save metadata so file metadata is accessible when docker restarts
def load_metadata():
    if os.path.exists("metadata.json"):
        with open("metadata.json", "r") as f:
            return json.load(f)
    return {}


def save_metadata(metadata_store):
    with open("metadata.json", "w") as f:
        json.dump(metadata_store, f)


metadata_store = load_metadata()


# Make sure it's an allowed file type
def allowed_file(filename):
    return any(filename.endswith(ext) for ext in ALLOWED_EXTENSIONS)


# Route to upload file
@app.route("/files", methods=["POST"])
@auth.login_required
def upload_file():

    # Make sure a file exists in the request
    if "file" not in request.files:
        return jsonify({"error": "No file found in request"}), 400

    # Get file from request
    file = request.files["file"]

    # Make sure file is of allowed type
    if not file or file.filename == "" or not allowed_file(file.filename):
        return jsonify({"error": "File must be .pdf, .jpg, .jpeg, or .png"}), 400

    # Generate unique ID
    file_id = str(uuid4())
    file_path = os.path.join(UPLOAD_FOLDER, f"{file_id}_{file.filename}")

    # Save file
    file.save(file_path)

    # Save metadata
    metadata = request.form.to_dict()
    metadata_store[file_id] = {
        "filename": file.filename,
        "filepath": file_path,
        "metadata": metadata,
    }

    save_metadata(metadata_store)

    # Return file id
    return jsonify({"file_id": file_id}), 201


# Route to retrieve a file by ID
@app.route("/files/<file_id>", methods=["GET"])
@auth.login_required
def get_file_by_id(file_id):

    # Get file from metadata
    file_record = metadata_store.get(file_id)

    # Check file exists
    if not file_record:
        return jsonify({"error": "File not found"}), 404

    # Return file
    return send_file(file_record["filepath"], as_attachment=True)


# Route to retrieve files by metadata tags
@app.route("/files", methods=["GET"])
@auth.login_required
def get_files_by_metadata():
    tag = request.args.get("tags")

    # If no tags are provided, return all files
    if not tag:
        return jsonify(list(metadata_store.values())), 200

    # Split the tag into key and value
    try:
        key, value = tag.split(":")
    except ValueError:
        return jsonify({"error": "Invalid tags format. Use key:value."}), 400

    # Filter files by key-value pair in metadata
    filtered_files = [
        file_info
        for file_info in metadata_store.values()
        if file_info["metadata"].get(key) == value
    ]

    # Return filtered files
    return jsonify(filtered_files), 200


# Route to delete a file
@app.route("/files/<file_id>", methods=["DELETE"])
@auth.login_required
def delete_file(file_id):

    # Pop file_id from metadata
    file_record = metadata_store.pop(file_id, None)

    # If nothing was popped from metadata, return file not found
    if not file_record:
        return jsonify({"error": "File not found"}), 404

    # Delete the file from the filesystem
    os.remove(file_record["filepath"])
    save_metadata(metadata_store)

    # Return successful deletion
    return jsonify({"status": "File deleted"}), 204


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

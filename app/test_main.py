import pytest
from main import app
from io import BytesIO


# Configure the test client fixture
@pytest.fixture
def client():
    app.config["TESTING"] = True
    client = app.test_client()
    yield client


# Create a fixture to upload a file and return its ID
@pytest.fixture
def uploaded_file_id(client):
    # Upload a dummy file and retrieve the file ID
    data = {
        "file": (BytesIO(b"%PDF-1.4 test content"), "testfile.pdf"),
        "category": "personal",
        "subject": "python",
    }
    response = client.post(
        "/files",
        data=data,
        headers={
            "Authorization": "Basic dXNlcjpwYXNzd29yZA=="
        },  # Base64 for "user:password"
    )
    assert response.status_code == 201  # Ensure the file upload is successful
    return response.get_json()["file_id"]  # Return the uploaded file ID for other tests


# Test retrieving the file by ID
def test_get_file_by_id(client, uploaded_file_id):
    response = client.get(
        f"/files/{uploaded_file_id}",
        headers={"Authorization": "Basic dXNlcjpwYXNzd29yZA=="},
    )
    assert response.status_code == 200
    assert response.headers["Content-Disposition"].startswith("attachment;")
    assert response.headers["Content-Type"] in [
        "application/pdf",
        "image/jpeg",
        "image/png",
    ]


# Test retrieving files by metadata
def test_get_files_by_metadata(client, uploaded_file_id):
    response = client.get(
        "/files?tags=category:personal",
        headers={"Authorization": "Basic dXNlcjpwYXNzd29yZA=="},
    )
    assert response.status_code == 200
    files = response.get_json()
    assert isinstance(files, list)
    assert any(file["metadata"].get("category") == "personal" for file in files)


# Test deleting the uploaded file
def test_delete_file(client, uploaded_file_id):
    # Delete the uploaded file
    response = client.delete(
        f"/files/{uploaded_file_id}",
        headers={"Authorization": "Basic dXNlcjpwYXNzd29yZA=="},
    )
    assert response.status_code == 204  # Verify deletion is successful

    # Check that the file is deleted by trying to retrieve it again
    response = client.get(
        f"/files/{uploaded_file_id}",
        headers={"Authorization": "Basic dXNlcjpwYXNzd29yZA=="},
    )
    assert response.status_code == 404  # Confirm that the file is no longer found


# Test unauthenticated access returns 401
def test_unauthenticated_access(client, uploaded_file_id):
    response = client.get(f"/files/{uploaded_file_id}")
    assert response.status_code == 401

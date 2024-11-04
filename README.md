# File Storage API

This project is a basic file storage API where users can securely upload, retrieve, and delete files. The API supports PDF and image file formats and allows users to attach metadata to files for easy retrieval by tags.

## Technologies Used

-   **Flask**: Flask is a Python framework used for creating REST APIs. It was chosen for its simplicity, flexibility, and ease of setup.

-   **Basic Authentication with Flask-HTTPAuth**: HTTP Basic Auth was implemented to secure the API endpoints with minimal setup.

-   **JSON for Metadata Storage**: Metadata is stored in a JSON file to ensure persistence even if the Docker container is restarted.

## Project Structure

```
.
├── app
│   ├── auth.py               # Handles user authentication using Basic Auth
│   ├── main.py               # Contains the API logic and routes
│   ├── Dockerfile            # Dockerfile to build the app container
│   ├── requirements.txt      # Python dependencies
│   ├── test_main.py          # Unit tests for API endpoints
│   └── uploads               # Directory for storing uploaded files
├── docker-compose.yml        # Docker Compose setup to run the application locally
└── README.md                 # Documentation
```

## Setup and Running

### Steps

1. **Build and Run the Application**:
   From the project root, use Docker Compose to build and start the service:

    ```bash
    docker-compose up
    ```

    This will start the Flask app on `localhost:8000`.

2. **Using the API**:
   You can interact with the API using tools like `curl` or Postman. Below are the main endpoints and usage examples.

## API Endpoints

### 1. **Upload a File**

-   **Endpoint**: `POST /files`
-   **Description**: Uploads a file with optional metadata.
-   **Allowed File Types**: `.pdf`, `.jpg`, `.jpeg`, `.png`
-   **Example**:
    ```bash
    curl -X POST "http://localhost:8000/files" -u user:password -F "file=@testfile.pdf" -F "category=personal" -F "subject=python"
    ```

### 2. **Retrieve a File by ID**

-   **Endpoint**: `GET /files/<file_id>`
-   **Description**: Fetches a file by its unique ID.
-   **Example**:
    ```bash
    curl -X GET "http://localhost:8000/files/<file_id>" -u user:password
    ```

### 3. **Retrieve Files by Metadata**

-   **Endpoint**: `GET /files?tags=category:personal`
-   **Description**: Fetches files that match specific metadata tags.
-   **Example**:
    ```bash
    curl -X GET "http://localhost:8000/files?tags=category:personal" -u user:password --output downloaded_file.pdf
    ```

### 4. **Delete a File**

-   **Endpoint**: `DELETE /files/<file_id>`
-   **Description**: Deletes a file by its unique ID.
-   **Example**:
    ```bash
    curl -X DELETE "http://localhost:8000/files/<file_id>" -u user:password
    ```

## Testing

Unit tests for each API endpoint are included to verify functionality. To run the tests:

1. Start the Docker container if not already running.
2. In a new terminal, execute:
    ```bash
    cd app
    pytest test_main.py
    ```

## Scalability Considerations

-   **File Storage**: In the future, file storage can be switched from local storage to a cloud storage solution (e.g., AWS S3). This would allow for greater storage capacity, redundancy, and performance optimization.
-   **Metadata Management**: Currently, metadata is stored in `metadata.json`, which is effective for small datasets. In the future, it could migrate to a database (e.g., PostgreSQL, MongoDB) to enable faster and more reliable querying of metadata.

-   **Authentication & Security**: The API uses Basic Authentication, which is sufficient for this use case. In a production setting, we'd integrate OAuth or API keys to enhance security further.

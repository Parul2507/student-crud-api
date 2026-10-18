# Student Management API

A Python backend application developed as part of the EWB Edu Tech internship project assignment. The application manages student records using FastAPI and SQLite and supports Create, Read, Update, and Delete (CRUD) operations.

## Features

- Create new student records
- Retrieve all students
- Retrieve an individual student by ID
- Update existing student details
- Delete student records
- Validate incoming request data
- Handle missing records and duplicate email addresses
- Persist data using SQLite
- Interactive API documentation with Swagger UI

## Technology Stack

- Python 3.10+
- FastAPI
- Uvicorn
- SQLite
- Pydantic

## Project Structure

```text
student-crud-api/
├── main.py
├── database.py
├── requirements.txt
├── .gitignore
└── README.md
```

The `students.db` file is generated locally when the database is initialized and is excluded from Git.

## Prerequisites

- Python 3.10 or newer
- pip
- Git (for cloning the repository)

## Installation

### 1. Clone the repository

Replace the URL below with the actual URL of this GitHub repository.

```bash
git clone https://github.com/Parul2507/student-crud-api.git
cd student-crud-api
```

### 2. Create a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use `.venv\Scripts\python.exe` in place of `python` in the commands below.

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

## Running the Application

From the project root, run:

```bash
python -m uvicorn main:app --reload
```

The API will be available at:

- Home endpoint: http://127.0.0.1:8000/
- Swagger UI: http://127.0.0.1:8000/docs

The database table is initialized by the application through `database.py`. Student records are stored in the local SQLite database.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Check API status |
| POST | `/students` | Create a student |
| GET | `/students` | Retrieve all students |
| GET | `/students/{student_id}` | Retrieve a student by ID |
| PUT | `/students/{student_id}` | Update a student's details |
| DELETE | `/students/{student_id}` | Delete a student |

## Student Fields

| Field | Type | Required |
|---|---|---|
| `id` | Integer | Generated automatically |
| `name` | String | Yes |
| `date_of_birth` | Date (`YYYY-MM-DD`) | Yes |
| `email` | String | Yes |
| `phone` | String | No |
| `course` | String | No |

Email addresses must be unique.

## Example Requests

### Create a student

**POST `/students`**

Request body:

```json
{
  "name": "Aarav Sharma",
  "date_of_birth": "2004-05-12",
  "email": "aarav@example.com",
  "phone": "9876543210",
  "course": "MCA"
}
```

Expected status: `201 Created`.

### Retrieve all students

**GET `/students`**

Returns a JSON list of student records.

### Retrieve one student

**GET `/students/1`**

Returns the student with ID `1`, if found.

### Update a student

**PUT `/students/1`**

Submit the complete set of editable fields:

```json
{
  "name": "Aarav Sharma",
  "date_of_birth": "2004-05-12",
  "email": "aarav@example.com",
  "phone": "9876543210",
  "course": "BCA"
}
```

Expected status: `200 OK`, if the update succeeds.

### Delete a student

**DELETE `/students/1`**

Deletes the student with ID `1`, if found.

## Error Handling

- `422 Unprocessable Entity`: Invalid request data or missing required fields
- `404 Not Found`: Student ID does not exist
- `409 Conflict`: Email address already belongs to another student

## Testing

1. Start the application.
2. Open http://127.0.0.1:8000/docs.
3. Test each endpoint using Swagger UI.
4. Verify that updates are reflected in subsequent GET requests.
5. Verify that deleted students cannot be retrieved.
6. Restart the application and check that previously saved records remain available.

## Security and Data

Use dummy student records for testing and demonstration. Do not commit real student personal information, passwords, API keys, or other secrets.

## Optional AI Extension

The assignment includes an optional local AI extension using Ollama. The core FastAPI and SQLite CRUD application is the required component; the AI extension is not included in this core implementation.

## Assignment

EWB Edu Tech Pvt. Ltd. — Internship Project Assignment: Python Backend Development.

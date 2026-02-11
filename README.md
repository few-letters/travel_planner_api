# Travel Planner API

A RESTful API for managing travel projects and places to visit using the Art Institute of Chicago API.

## Tech Stack

- **Language:** Python 3.11
- **Framework:** Django 5
- **API Toolkit:** Django REST Framework
- **Database:** SQLite (default)
- **External Requests:** Requests (library)

## Setup & Installation

Follow these steps to set up and run the project locally.

### 1. Clone the repository

```bash
git clone https://github.com/few-letters/travel_planner_api
cd travel_planner
```

### 2. Create and activate a virtual environment

**Git Bash:**
```bash
python -m venv venv
source venv/Scripts/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply migrations

```bash
python manage.py migrate
```

### 5. Create a superuser (Required for basic auth)

```bash
python manage.py createsuperuser
# Example credentials:
# Username: admin
# Password: admin123
```

### 6. Run the server

```bash
python manage.py runserver
```

### The API will be available at `http://127.0.0.1:8000/api/`.

## API Documentation (Postman)

A Postman collection is included **`Travel_Planner.postman_collection.json`**.
The collection is pre-configured with Basic Auth (`admin` / `admin123`). 

### Key Endpoints

#### Projects
- **POST** `/api/projects/` - Create a new project (supports nested `places` list).
- **GET** `/api/projects/` - List all projects with their completion status.
- **GET** `/api/projects/{id}/` - Retrieve a single project.
- **DELETE** `/api/projects/{id}/` - Delete a project (allowed only if no places are visited).

#### Places
- **GET** `/api/places/?project_id={id}` - List places for a specific project.
- **POST** `/api/places/` - Add a new place to an existing project (Body must include `project` ID).
- **PATCH** `/api/places/{id}/` - Mark a place as visited (`is_visited: true`) or update notes.
- **GET** `/api/places/?project_id={id}` - List places for a specific project.
- **PATCH** `/api/places/{id}/` - Mark a place as visited (`is_visited: true`) or update notes.

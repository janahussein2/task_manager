# Task Manager Application

A full-stack Task Management System built with **FastAPI** (backend) and **Streamlit** (frontend). This application allows teams to manage users and tasks with role-based access, priority levels, and comprehensive filtering capabilities.

## Features

- **User Management**: Create and manage users with roles (admin, manager, team member) and profile information
- **Task Management**: Create, update, delete, and filter tasks with validation
- **Data Validation**: Strict validation rules (e.g., task titles must be capitalized, priority levels from predefined set)
- **RESTful API**: Modular FastAPI backend with separate routers for users and tasks
- **Interactive UI**: Beautiful Streamlit dashboard with colorful styling and real-time updates

## Prerequisites

- Python 3.12 or higher
- [uv](https://github.com/astral-sh/uv) package manager installed

## Project Structure

```
task_manager/
├── main.py              # FastAPI application entry point
├── app.py               # Streamlit frontend application
├── pyproject.toml       # Project dependencies and configuration
├── routers/
│   ├── users.py        # User management endpoints
│   └── tasks.py        # Task management endpoints
├── schemas/
│   └── models.py       # Pydantic models and validators
├── users.json          # User data storage (auto-created)
└── tasks.json          # Task data storage (auto-created)
```

## Setup Instructions

### 1. Install Dependencies

First, sync all project dependencies using `uv`:

```bash
uv sync
```

This command will:
- Create a virtual environment (if it doesn't exist)
- Install all dependencies listed in `pyproject.toml`
- Install development dependencies (if any)

## Running the Application

This application consists of two components that need to run simultaneously:

### 1. Start the FastAPI Backend Server

In your first terminal window, run:

```bash
uv run fastapi dev main.py
```

The FastAPI server will start on `http://localhost:8000`

**Available endpoints:**
- `GET /` - API welcome message
- `GET /users/` - Get all users
- `POST /users/` - Create a new user
- `GET /tasks/` - Get all tasks (with optional filters: `?status=`, `?priority=`, `?assigned_to=`)
- `POST /tasks/` - Create a new task
- `PATCH /tasks/{task_id}/status?status_update={status}` - Update task status
- `DELETE /tasks/{task_id}` - Delete a task

**API Documentation:**
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### 2. Start the Streamlit Frontend

In your second terminal window, run:

```bash
streamlit run app.py
```

The Streamlit app will automatically open in your browser at `http://localhost:8501`

**Note:** Make sure the FastAPI server is running before starting Streamlit, as the frontend connects to the API at `http://localhost:8000`.

## Usage

### Creating Users

1. Navigate to the "Create User" tab in the Streamlit app
2. Fill in the required fields:
   - **Name**: User's full name
   - **Role**: Select from admin, manager, or team member
   - **Email**: User's email address (required)
   - **Phone**: Optional phone number
3. Click "Create User"

### Creating Tasks

1. Navigate to the "Create Task" tab
2. Fill in the required fields:
   - **Title**: Task title (must start with a capital letter)
   - **Description**: Detailed task description
   - **Priority**: Select from low, medium, or high
   - **Status**: Task status (e.g., pending, in_progress, completed)
   - **Assigned To**: Optional user assignment
3. Click "Create Task"

### Viewing and Managing Tasks

- Use the "View Tasks" tab to see all tasks
- Filter tasks by status, priority, or assigned user
- Update task status using the dropdown menu
- Delete tasks using the delete button

## Data Validation Rules

- **Task Titles**: Must start with a capital letter
- **Priority Levels**: Must be one of: `low`, `medium`, `high`
- **User Roles**: Must be one of: `admin`, `manager`, `team member`

## Data Storage

The application uses JSON files for data persistence:
- `users.json` - Stores all user data
- `tasks.json` - Stores all task data

These files are automatically created when you first create a user or task. The data persists between application restarts.

## Development

### Running with Auto-reload

Both servers support auto-reload during development:
- FastAPI: Already configured with `--reload` flag
- Streamlit: Automatically reloads on file changes

### Testing the API

You can test the API endpoints using:
- The Swagger UI at `http://localhost:8000/docs`
- The Streamlit frontend
- Any HTTP client (curl, Postman, etc.)

Example API call:

```bash
# Create a user
curl -X POST "http://localhost:8000/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "role": "admin",
    "profile": {
      "email": "john@example.com",
      "phone": "+1234567890"
    }
  }'
```

## Troubleshooting

### Port Already in Use

If port 8000 or 8501 is already in use:

**FastAPI:**
```bash
uv run fastapi dev main.py --port 8001
```

**Streamlit:**
```bash
streamlit run app.py --server.port 8502
```

Don't forget to update the `API_BASE_URL` in `app.py` if you change the FastAPI port.

### Module Not Found Errors

Make sure you've:
1. Run `uv sync`
2. Activated the virtual environment
3. Are running commands from the project root directory

### API Connection Errors

If Streamlit can't connect to FastAPI:
- Ensure FastAPI is running on `http://localhost:8000`
- Check the `API_BASE_URL` in `app.py` matches your FastAPI server URL
- Verify no firewall is blocking the connection

## License

This project is part of a bootcamp assignment.

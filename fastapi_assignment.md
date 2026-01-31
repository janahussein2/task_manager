## Student Assignment: Building a Modular API with FastAPI

### Project Overview

In this assignment, you will develop a **Task Management System** backend using FastAPI. This project focuses on structuring a professional-grade API using modern Python type hinting, modular routing, and robust data validation with Pydantic.

---

### Application Goal

The **Task Management System** is a RESTful API backend designed to help teams and individuals organize, track, and manage their work tasks. The application serves as the foundation for a collaborative task management platform where:

**Core Functionality:**
- **User Management**: Register and manage users with different roles (e.g., admin, manager, team member) and profile information
- **Task Management**: Create, update, tasks with attributes like title, description, priority level, status, and assignment to users
- **Data Validation**: Ensure data integrity through strict validation rules (e.g., task titles must be capitalized, priority levels must be from a predefined set)
- **Query Capabilities**: Filter and search tasks by various criteria (status, priority, assigned user, etc.)

**Real-World Use Case:**
Imagine a development team using this API to track sprint tasks, a project manager assigning work items to team members, or a personal productivity app managing daily to-dos. The API provides the backend infrastructure that a frontend application (web or mobile) would consume to display and interact with tasks and users.

**Key Features:**
- Users can be created with profiles containing contact information and role assignments
- Tasks can be created with validation ensuring proper formatting and valid priority levels
- The API supports filtering and querying to find specific tasks or users
- All data is validated at the API layer before processing, ensuring consistency and preventing invalid data from entering the system

---

### Learning Objectives

By the end of this project, you will be able to:

* Organize code into logical modules using `APIRouter`.
* Enforce data integrity using Pydantic `BaseModel` and `@field_validator`.
* Implement complex data structures with **Nested Models**, `Literal`, and `Annotated`.
* Handle various HTTP methods and parameter types.

---

### Project Structure

To maintain scalability, follow this directory structure:

```text
task_manager/
├── main.py
├── routers/
│   ├── users.py
│   └── tasks.py
└── schemas/
    └── models.py

```

---

### Phase 1: Data Modeling (Schemas)

In `schemas/models.py`, define the data shapes. You must use `Annotated` for metadata and `@field_validator` for custom logic.

```python
from pydantic import BaseModel, Field, field_validator
from typing import List, Literal, Annotated

class Profile(__BLANK__):
    __BLANK__

class UserCreate(__BLANK__):
    __BLANK__

class TaskCreate(__BLANK__):
    __BLANK__

    @field_validator('title')
    @classmethod
    def title_must_be_capitalized(cls, v: str) -> str:
        __BLANK__
```

*Source: [Pydantic Documentation on Validators*](https://docs.pydantic.dev/latest/concepts/validators/)

---

### Phase 2: Modular Routing

Create separate routers for `users` and `tasks`. Use `APIRouter` to group these endpoints.

**Example: `routers/tasks.py**`

```python
from fastapi import APIRouter, Query
from typing import Annotated
from schemas.models import TaskCreate

router = __BLANK__

@router.get("/")
async def __BLANK_

@router.post("/")
async def __BLANK__

```

*Source: [FastAPI Documentation on Bigger Applications*](https://fastapi.tiangolo.com/tutorial/bigger-applications/)

---

### Phase 3: Application Assembly

In `main.py`, initialize the FastAPI app and include your routers.

```python
from fastapi import FastAPI
from routers import users, tasks

app = __BLANK__

# Include the routers
app.__BLANK__
app.__BLANK__

@app.get("/")
async def root():
    return {"message": "Welcome to the Task API"}

```

---

### Submission Requirements

1. **Codebase:** A GitHub link containing the completed modules.
2. **Validation Test:** Provide a screenshot of the `/docs` (Swagger UI) showing a successful `POST` request to `/tasks` that passes the `@field_validator` logic.
3. **Error Handling:** Provide a screenshot of the 422 Unprocessable Entity error when the `Literal` role or `Annotated` priority constraints are violated.

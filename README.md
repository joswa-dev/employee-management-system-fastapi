# Employee Management System API

A secure Employee Management System built using FastAPI.

## Features
- JWT Login Authentication
- Role-Based Authorization
- Add Employee (Admin only)
- Update Employee (Admin only)
- Delete Employee (Admin only)
- Get Employee by ID
- Search Employee by Name

## Tech Stack
- Python
- FastAPI
- SQLAlchemy
- JWT Authentication
- SQLite
- Swagger UI

## Run Locally

Install dependencies:

```bash
pip install -r requirements.txt
```

Run server:

```bash
uvicorn main:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Employee
from app.schemas import EmployeeCreate, EmployeeLogin
from app.auth import (
    create_access_token, 
    verify_token,
    verify_password,
    hash_password
)

router = APIRouter()


# Register Employee
@router.post("/register")
def register_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):

    existing_employee = db.query(Employee).filter(
        Employee.email == employee.email
    ).first()

    if existing_employee:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    new_employee = Employee(
        name=employee.name,
        email=employee.email,
        position=employee.position,
        department=employee.department,
        password=hash_password(employee.password),
        role=employee.role
    )

    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)

    return {"message": "Employee registered successfully"}


# Login
@router.post("/login")
def login(employee: EmployeeLogin, db: Session = Depends(get_db)):

    user = db.query(Employee).filter(
        Employee.email == employee.email
    ).first()

    if not user or not verify_password(
        employee.password,
        user.password

    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    token = create_access_token(
        data={
            "sub": user.email,
            "role": user.role
        }
    )
    return {
        "message": "Login successful",
        "employee": user.name,
        "access_token": token,
        "token_type": "bearer"
    }


# Get All Employees
@router.get("/employees")
def get_employees(
    user: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    if user.get("role") != "admin":
        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )

    employees = db.query(Employee).all()

    return [
        {
            "id": emp.id,
            "name": emp.name,
            "email": emp.email,
            "position": emp.position,
            "department": emp.department,
            "role": emp.role
        }
        for emp in employees
    ]

    return employees

# Get Employee By ID
# Search Employee by Name
@router.get("/employees/search")
def search_employee(
    name: str,
    user: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    
     # Admin only
    if user.get("role") != "admin":
        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )

    employees = db.query(Employee).filter(
        Employee.name.ilike(f"%{name}%")
    ).all()

    if not employees:
        raise HTTPException(
            status_code=404,
            detail="No employees found"
        )

    return [
        {
            "id": emp.id,
            "name": emp.name,
            "email": emp.email,
            "position": emp.position,
            "department": emp.department,
            "role": emp.role
        }
        for emp in employees
    ]

@router.get("/employees/{employee_id}")
def get_employee_by_id(
    employee_id: int,
    user: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):

    # Admin only
    if user.get("role") != "admin":
        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )

    employee = db.query(Employee).filter(
        Employee.id == employee_id
    ).first()

    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    return {
        "id": employee.id,
        "name": employee.name,
        "email": employee.email,
        "position": employee.position,
        "department": employee.department,
        "role": employee.role
    }


# Add Employee (Admin Only)
@router.post("/employees")
def add_employee(
    employee: EmployeeCreate,
    user: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    # Only admin can add employees
    if user.get("role") != "admin":
        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )

    existing_employee = db.query(Employee).filter(
        Employee.email == employee.email
    ).first()

    if existing_employee:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    new_employee = Employee(
        name=employee.name,
        email=employee.email,
        position=employee.position,
        department=employee.department,
        password=hash_password(employee.password),
        role=employee.role
    )

    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)

    return {
        "message": "Employee added successfully"
    }

# Update Employee (Admin Only)
@router.put("/employees/{employee_id}")
def update_employee(
    employee_id: int,
    employee: EmployeeCreate,
    user: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):
    # Admin only
    if user.get("role") != "admin":
        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )

    existing_employee = db.query(Employee).filter(
        Employee.id == employee_id
    ).first()

    if not existing_employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    existing_employee.name = employee.name
    existing_employee.email = employee.email
    existing_employee.position = employee.position
    existing_employee.department = employee.department
    existing_employee.password = hash_password(employee.password)
    existing_employee.role = employee.role

    db.commit()
    db.refresh(existing_employee)

    return {
        "message": "Employee updated successfully"
    }

# Delete Employee (Admin only)
@router.delete("/employees/{employee_id}")
def delete_employee(
    employee_id: int,
    user: dict = Depends(verify_token),
    db: Session = Depends(get_db)
):

    # Only admin can delete
    if user.get("role") != "admin":
        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )

    employee = db.query(Employee).filter(
        Employee.id == employee_id
    ).first()

    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    db.delete(employee)
    db.commit()

    return {
        "message": "Employee deleted successfully"
    }
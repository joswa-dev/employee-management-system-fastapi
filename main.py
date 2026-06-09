from fastapi import FastAPI

from app.database import engine, Base
from app.routes import router
from app.database import SessionLocal
from app.models import Employee
from app.auth import hash_password # or wherever your hash function is

Base.metadata.create_all(bind=engine)

db = SessionLocal()

admin = db.query(Employee).filter(
    Employee.email == "admin@gmail.com"
).first()

if not admin:
    admin_user = Employee(
        name="admin1",
        email="admin@gmail.com",
        password=hash_password("admin123"),
        position="Developer",
        department="IT",
        role="admin"
    )

    db.add(admin_user)
    db.commit()

db.close()

app = FastAPI(
    title="Employee Management System"
)

app.include_router(router)


@app.get("/")
def home():
    return {"message": "Employee Management API Running"}
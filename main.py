from fastapi import FastAPI

from app.database import engine, Base
from app.routes import router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Employee Management System"
)

app.include_router(router)


@app.get("/")
def home():
    return {"message": "Employee Management API Running"}
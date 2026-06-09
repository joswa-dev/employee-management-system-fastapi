from pydantic import BaseModel


class EmployeeCreate(BaseModel):
    name: str
    email: str
    position: str
    department: str
    password: str
    role: str


class EmployeeLogin(BaseModel):
    email: str
    password: str
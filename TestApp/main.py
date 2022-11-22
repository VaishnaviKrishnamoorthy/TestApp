from fastapi import FastAPI, HTTPException
from typing import List
from uuid import UUID
from typing import Optional, List
from pydantic import BaseModel
from uuid import UUID,uuid4
from enum import Enum


app = FastAPI()

class Gender(str, Enum):
    male = "male"
    female = "female"

class Role(str, Enum):
    student = "student"
    admin = "admin"
    user = "user"

class User(BaseModel):
    id: Optional[UUID] = uuid4()
    first_name: str
    last_name: str
    middle_name: Optional[str]
    gender: Gender
    roles: List[Role]

db: List[User] = [
    User(id=UUID("87cd0b62-a93a-4764-b064-df656cb2e039"),
    first_name="vaishu",
    last_name="krishnamoorthy",
    gender= Gender.female,
    roles= [Role.student]
    ),
    User(id=UUID("b09fca1b-0b9e-4931-9eec-eee1d0ca5066"),
    first_name="vishu",
    last_name="gowtham",
    gender= Gender.male,
    roles= [Role.admin, Role.user]
    )
]

@app.get("/")
async def root():
    return{"hello":"vaishu"}

@app.get("/api/v1/users")
async def fetch_user():
    return db;
    
@app.post("/api/v1/users")
async def register_user(user: User):
    db.append(user)
    return {"id": user.id}

@app.delete("/api/v1/users/{user_id}")
async def delete_user(user_id: UUID):
    for user in db:
        if user.id == user_id:
            db.remove(user)
            return

    raise HTTPException (
        status_code=404,
        detail=f"user with id: {user_id} does not exists"
    )  
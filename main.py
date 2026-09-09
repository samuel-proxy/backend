from fastapi import FastAPI, HTTPException
from supabase import create_client  # type: ignore[import-not-found]
from dotenv import load_dotenv
import os
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY"),
)

class User(BaseModel):
    username: str
    password: str
    


@app.post("/users")
def add_student(user: User):
    response = supabase \
        .table("users") \
        .insert(user.model_dump()) \
        .execute()
    return response.data

@app.post("/login")
def login(user: User):
    response = supabase \
        .table("users") \
        .select("*") \
        .eq("username", user.username) \
        .eq("password", user.password) \
        .execute()
    if len(response.data) == 0:
        raise HTTPException(
            status_code=401,
            detail = "Invalid username or password"
        )
    
    return{
        "message": "Login successful",
        "user": response.data[0]
    }
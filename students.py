from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




class Student(BaseModel):
    name: str
    age: int
    course: str

students = [] #temporary storage

@app.post("/students")
def add_student(student: Student):
    students.append(student)
    return {
            "message": "Student created successfully",
            "student": student    
        }

#get all students
@app.get("/students")
def get_students():
    return students
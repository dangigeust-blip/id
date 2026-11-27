from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel ,field_validator, EmailStr
import psycopg2
import uuid
import re
app = FastAPI()

#to connect database
def db_connection(): 
    return psycopg2.connect(
        host= "localhost",
        user= "postgres",
        database= "student_db",
        password= "admin123",
    )
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class student(BaseModel):
    student_name: str
    mobile_no:str
    email: EmailStr 
    course: str

    @field_validator("student_name")
    @classmethod
    def check_name(cls, value):
        if not value.isalpha():
            raise ValueError("Name must contain only alphabets")
        return value

    @field_validator("mobile_no")
    @classmethod
    def check_number(cls, value):

        if not re.fullmatch(r"91[0-9]{10}", value):
            raise ValueError("Number must start with 91 and contain 12 digits")

        return value

@app.get("/")
def display():
    return{
        "message":"api is running"
    }

@app.post("/register")
def register_student(student: student):

    connection = db_connection()
    cursor = connection.cursor()
  
    
    unique_id = f"AIM-{uuid.uuid4().hex[:8].upper()}"
    query = """
        INSERT INTO students
        (unique_id, student_name, mobile_no, Email, course)
        VALUES (%s, %s, %s, %s, %s)
    """
   
    values = (
        unique_id,
        student.student_name,
        student.mobile_no,
        student.email,
        student.course
    )
#mobile no check
    cursor.execute(
                "SELECT unique_id FROM students WHERE mobile_no = %s",
                (student.mobile_no,)
            )
    
    mobile = cursor.fetchone()

    if mobile:
        cursor.close()
        connection.close()
        return {"message": "Mobile number already registered"}
   #Email check
    cursor.execute(
            "SELECT unique_id FROM students WHERE email = %s",
            (student.email,)
        )
    email = cursor.fetchone()

    if email:
        cursor.close()
        connection.close()
        return {"message": "Email already registered"}
    cursor.execute(query, values)
    connection.commit()
    
    cursor.close()
    connection.close()

    return {
        "message": "Student registered successfully",
        "unique_id": unique_id
    }

import sqlite3
from datetime import date

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from database import get_connection

app = FastAPI(title="Student Management API")


# Request model: validates incoming student details
class StudentCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    date_of_birth: date
    email: str = Field(
        pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    )
    phone: str | None = Field(default=None, max_length=20)
    course: str | None = Field(default=None, max_length=100)


# Response model: defines the data returned by the API
class StudentResponse(StudentCreate):
    id: int


@app.get("/")
def home():
    return {"message": "Student Management API is running"}


@app.post("/students", response_model=StudentResponse, status_code=201)
def create_student(student: StudentCreate):
    conn = get_connection()

    try:
        cursor = conn.execute(
            """
            INSERT INTO students
                (name, date_of_birth, email, phone, course)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                student.name,
                student.date_of_birth.isoformat(),
                student.email,
                student.phone,
                student.course,
            ),
        )

        conn.commit()

        row = conn.execute(
            "SELECT * FROM students WHERE id = ?",
            (cursor.lastrowid,),
        ).fetchone()

        return dict(row)

    except sqlite3.IntegrityError:
        conn.rollback()
        raise HTTPException(
            status_code=409,
            detail="A student with this email already exists",
        )

    finally:
        conn.close()

@app.get("/students", response_model=list[StudentResponse])
def get_students():
    conn = get_connection()

    try:
        rows = conn.execute(
            "SELECT * FROM students ORDER BY id"
        ).fetchall()

        return [dict(row) for row in rows]

    finally:
        conn.close()


@app.get("/students/{student_id}", response_model=StudentResponse)
def get_student(student_id: int):
    conn = get_connection()

    try:
        row = conn.execute(
            "SELECT * FROM students WHERE id = ?",
            (student_id,),
        ).fetchone()

        if row is None:
            raise HTTPException(
                status_code=404,
                detail="Student not found",
            )

        return dict(row)

    finally:
        conn.close()

@app.put("/students/{student_id}", response_model=StudentResponse)
def update_student(student_id: int, student: StudentCreate):
    conn = get_connection()

    try:
        # Check whether the student exists
        existing_student = conn.execute(
            "SELECT id FROM students WHERE id = ?",
            (student_id,),
        ).fetchone()

        if existing_student is None:
            raise HTTPException(
                status_code=404,
                detail="Student not found",
            )

        # Update the existing student
        conn.execute(
            """
            UPDATE students
            SET name = ?,
                date_of_birth = ?,
                email = ?,
                phone = ?,
                course = ?
            WHERE id = ?
            """,
            (
                student.name,
                student.date_of_birth.isoformat(),
                student.email,
                student.phone,
                student.course,
                student_id,
            ),
        )

        conn.commit()

        # Retrieve the updated record
        updated_student = conn.execute(
            "SELECT * FROM students WHERE id = ?",
            (student_id,),
        ).fetchone()

        return dict(updated_student)

    except sqlite3.IntegrityError:
        conn.rollback()
        raise HTTPException(
            status_code=409,
            detail="A student with this email already exists",
        )

    finally:
        conn.close()

@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    conn = get_connection()

    try:
        # Check whether the student exists
        existing_student = conn.execute(
            "SELECT id FROM students WHERE id = ?",
            (student_id,),
        ).fetchone()

        if existing_student is None:
            raise HTTPException(
                status_code=404,
                detail="Student not found",
            )

        # Delete the student
        conn.execute(
            "DELETE FROM students WHERE id = ?",
            (student_id,),
        )

        conn.commit()

        return {
            "message": "Student deleted successfully",
            "student_id": student_id,
        }

    finally:
        conn.close()

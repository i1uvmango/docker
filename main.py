from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, validator
from typing import List

app = FastAPI()

grade_to_score = {
    "A+": 4.5, "A": 4.0, "B+": 3.5, "B": 3.0,
    "C+": 2.5, "C": 2.0, "D+": 1.5, "D": 1.0, "F": 0.0
}

class Course(BaseModel):
    course_code: str
    course_name: str
    credits: int
    grade: str

    @validator('grade')
    def check_grade(cls, v):
        if v not in grade_to_score:
            raise ValueError("Invalid grade")
        return v

class StudentRequest(BaseModel):
    student_id: str
    name: str
    courses: List[Course]

@app.post("/score")
def get_summary(data: StudentRequest):
    total_credits = sum(c.credits for c in data.courses)
    total_points = sum(c.credits * grade_to_score[c.grade] for c in data.courses)
    gpa = round(total_points / total_credits + 1e-8, 3)

    return {
        "student_summary": {
            "student_id": data.student_id,
            "name": data.name,
            "gpa": round(gpa, 2),
            "total_credits": total_credits
        }
    }

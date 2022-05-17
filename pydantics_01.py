from pydantic import BaseModel, Field
from typing import List
from enum import Enum

class Classes(str, Enum):
    PHYS101 = "Physics I"
    PHYS125 = "Calculational Methods In Physics"
    PHYS150 = "Information and Entropy"

class Student(BaseModel):
    name: str = Field(default=None, max_length=50, min_length=3)
    email: str = Field(default=None, max_length=50, min_length=3)
    faculty: str = Field(default=None, max_length=50, min_length=3)
    classes: List[Classes]
    grade: int = Field(default=1, gt=0, lt=5)

student_data1 = {
    "name": "student1",
    "email": "user@example.com",
    "faculty": "Physics",
    "classes": [Classes.PHYS101, Classes.PHYS150],
    "grade": 4
}

student1 = Student(**student_data1)

print(student1)
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
import json

class ExerciseSet(BaseModel):
    reps: int
    weight: Optional[float]

class Exercise(BaseModel):
    name: str
    series: List[ExerciseSet]

class WorkoutDay(BaseModel):
    exercises: List[Exercise]

class StudentWorkoutPlan(BaseModel):
    Monday: Optional[List[Exercise]] = None
    Tuesday: Optional[List[Exercise]] = None
    Wednesday: Optional[List[Exercise]] = None
    Thursday: Optional[List[Exercise]] = None
    Friday: Optional[List[Exercise]] = None
    Saturday: Optional[List[Exercise]] = None
    Sunday: Optional[List[Exercise]] = None

class StudentModel(BaseModel):
    user_id: str
    user_type: str
    email: str
    workout_plan: Optional[StudentWorkoutPlan] = None



def save_student_model_to_json(student_model: StudentModel, file_path: str):
    data = student_model.dict()
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, indent=2)

# Example usage:
student_data = {
    "user_id": "123",
    "user_type": "athlete",
    "email": "athlete@example.com",
    "workout_plan": {
        "Monday": [],
        "Tuesday": [],
        "Wednesday": [], 
        "Thursday": [],
        "Friday": [],
        "Saturday": [],
        "Sunday": []
    }
}

student_model_instance = StudentModel(**student_data)
save_student_model_to_json(student_model_instance, 'student_model.json')
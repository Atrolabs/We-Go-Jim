from datetime import datetime
from pydantic import BaseModel
from typing import List

class ExerciseSet(BaseModel):
    number: int
    reps: int
    weight: float

class Exercise(BaseModel):
    name: str
    sets: List[ExerciseSet]

class UserModel(BaseModel):
    """Initialize user model script on registration"""
    user_sub: str
    last_modified: str = str(datetime.utcnow())

class UserExerciseModel(UserModel):
    workout_plan: List[List[Exercise]]

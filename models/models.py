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

class DayWorkout(BaseModel):
    day_name: str
    exercises: List[Exercise]

class UserModel(BaseModel):
    user_sub: str
    last_modified: str = str(datetime.utcnow())

class UserExerciseModel(UserModel):
    workout_plan: List[DayWorkout] = [
        {"day_name": "Monday", "exercises": []},
        {"day_name": "Tuesday", "exercises": []},
        {"day_name": "Wednesday", "exercises": []},
        {"day_name": "Thursday", "exercises": []},
        {"day_name": "Friday", "exercises": []},
        {"day_name": "Saturday", "exercises": []},
        {"day_name": "Sunday", "exercises": []}
    ]

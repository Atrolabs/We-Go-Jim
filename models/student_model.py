from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

class ExerciseSet(BaseModel):
    reps: int
    weight: Optional[float]

class Exercise(BaseModel):
    sets: List[ExerciseSet]

class WorkoutDay(BaseModel):
    exercises: List[Exercise]

class UserWorkoutPlan(BaseModel):
    Monday: Optional[WorkoutDay] = None
    Tuesday: Optional[WorkoutDay] = None
    Wednesday: Optional[WorkoutDay] = None
    Thursday: Optional[WorkoutDay] = None
    Friday: Optional[WorkoutDay] = None
    Saturday: Optional[WorkoutDay] = None
    Sunday: Optional[WorkoutDay] = None

class UserModel(BaseModel):
    user_id: str
    user_type: str
    creation_date: datetime = datetime.now()
    workout_plan: UserWorkoutPlan = UserWorkoutPlan()

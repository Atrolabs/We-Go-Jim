curl -X POST -H "Content-Type: application/json" -d '{
  "user_id": "your-user-id",
  "workout_data": [
    {"day_name": "Thursday", "exercises": [
      {"name": "Exercise1", "sets": [{"number": 1, "reps": 10, "weight": 50.0}, {"number": 2, "reps": 8, "weight": 60.0}, {"number": 3, "reps": 12, "weight": 40.0}]},
      {"name": "Exercise2", "sets": [{"number": 1, "reps": 12, "weight": 45.0}, {"number": 2, "reps": 10, "weight": 55.0}, {"number": 3, "reps": 8, "weight": 65.0}]},
      {"name": "Exercise3", "sets": [{"number": 1, "reps": 8, "weight": 70.0}, {"number": 2, "reps": 12, "weight": 40.0}, {"number": 3, "reps": 10, "weight": 55.0}]}
    ]}
  ]
}' http://your.local.host.ip:port/add-workout
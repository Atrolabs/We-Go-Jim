curl -X POST -H "Content-Type: application/json" -d '{
  "user_sub": "yoursub",
  "records": [
    {"name": "Bench Press", "record_list": [{"weight": 200.0}]}
  ]
}' http://127.0.0.1:5000/test
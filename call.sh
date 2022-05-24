# curl -H "Content-type: application/json" -X POST localhost:8000/api/users --data '{"username":"john", "password": "eightyeight"}'

curl -H "accept: application/json" -H "Content-Type: application/x-www-form-urlencoded" -X POST localhost:8000/api/login -d 'username=john&password=eightyeight'



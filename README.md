To run project just run
```shell
docker-compose up -d
```

You will get three containers:
- backend
- frontend
- db

At first run db is empty, you will need to populate.
To do so just run **inside** backend container this command
```shell
poetry run python3 ./scripts/__init__.py
```

Now app is ready to go!
Here's some information:
1. DB is reachable under postgresql://username:password@db:5432/api
2. Backend API is reachable under http://localhost:5001
3. Frontend App is reachable under http://localhost:5173
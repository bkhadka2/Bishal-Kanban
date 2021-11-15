# Kanban
Project to create a kanban using Python flask

# How to run the app
```bash
Git clone the project
Open your terminal
Set the path: export FLASK_RUN=app
Set the development path: export FLASK_ENV=development
Type the command flask run
It should run on localhost/5000
```

# If database not found error
```python
Open your terminal in the same window where app.py is
Type python3
Type: from app import db
Type: db.create_all()
Type: exit()
Type: flask run
```

# Screenshots of app running
![App running 0](./screenshots/app_running.png)
![App running 1](./screenshots/app_running1.png)

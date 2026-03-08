# Assignment Tracker

Assignment Tracker is a simple Flask + MySQL web app for students to manage subjects and assignments. It supports registration and login, adding subjects and assignments, and tracking assignment status through a dashboard.

## Features
- Student registration and login
- Personal dashboard listing assignments with subject and due date
- Add subjects and assignments
- Mark assignments as completed
- Delete assignments

## Tech Stack
- Python (Flask)
- MySQL
- Jinja2 templates

## Project Structure
- `app.py` Flask app and routes
- `templates/` HTML templates (login, register, dashboard, subject, assignment)
- `static/` static assets (CSS/JS/images if any)
- `config.py` database configuration (not committed)
- `config_example.py` sample DB configuration

## Setup
1. Create a virtual environment and install dependencies.
2. Configure the database connection.
3. Initialize the database schema.
4. Run the Flask app.

### 1) Create a virtual environment and install dependencies
```powershell
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

### 2) Configure the database connection
Copy `config_example.py` to `config.py` and update the values:
```powershell
Copy-Item config_example.py config.py
```

### 3) Initialize the database schema
Create a MySQL database and the required tables. A minimal schema:
```sql
CREATE TABLE students (
  student_id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  email VARCHAR(255) NOT NULL UNIQUE,
  password VARCHAR(255) NOT NULL
);

CREATE TABLE subjects (
  subject_id INT AUTO_INCREMENT PRIMARY KEY,
  subject_name VARCHAR(100) NOT NULL,
  student_id INT NOT NULL,
  FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE
);

CREATE TABLE assignments (
  assignment_id INT AUTO_INCREMENT PRIMARY KEY,
  title VARCHAR(255) NOT NULL,
  due_date DATE NOT NULL,
  status VARCHAR(20) NOT NULL DEFAULT 'Pending',
  subject_id INT NOT NULL,
  FOREIGN KEY (subject_id) REFERENCES subjects(subject_id) ON DELETE CASCADE
);
```

### 4) Run the app
```powershell
python app.py
```

Then open `http://127.0.0.1:5000/` in your browser.

## Usage
- Register a student account
- Add subjects
- Add assignments to subjects
- Mark assignments as completed or delete them

## Notes
- `app.secret_key` is hardcoded in `app.py`. For production, use an environment variable.

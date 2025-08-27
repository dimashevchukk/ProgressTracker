# Progress Tracker

Progress Tracker is a personal content tracking application built with **Django**.  
It helps users keep track of books, movies, games, and series, monitor progress, add notes, rate keep track on story and don't lose your thoughts.  
The app is designed as both a practical tool and a portfolio project.

---

## URL https://progresstracker-i1rf.onrender.com/

---

## Features

- User authentication
- Add and manage media items
- Track progress
- Rate
- Write notes and personal thoughts
- Organize items with tags and categories
- Simple dashboard to view your current progress

---

## Tech Stack

- **Backend:** Django, Python
- **Database:** SQLite

---

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/dimashevchukk/progress-tracker.git
    cd progress-tracker

2. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate    # On Linux/Mac
    venv\Scripts\activate       # On Windows

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
   
4. Set up environment variables.
Create a .env file in the project root:
    ```bash
    SECRET_KEY=your-django-secret-key
   
5. Run migrations:
    ```bash
    python manage.py migrate
   
6. Start local server:
    ```bash
    python manage.py runserver

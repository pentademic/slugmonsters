# SlugMonsters

A Django web application built as a learning project.

## Tech Stack

- **Python** + **Django 2.2**
- SQLite (default)

## Project Structure

```
slugmonsters/
├── mysite/              Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── slugmonsters/        Main app
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   ├── templates/
│   └── static/
├── manage.py
└── requirements.txt
```

## Installation

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Then open http://127.0.0.1:8000/

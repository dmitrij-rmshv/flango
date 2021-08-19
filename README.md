# flango

### Educational mini web framework (like django, flask) and application on it.

Для запуска приложения:

    uwsgi --http :8000 --wsgi-file run_app.py
либо

    gunicorn run_app:application

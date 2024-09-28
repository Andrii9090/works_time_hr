# REST API for service for recording work time

## Overview

This API is used to record work time of workers.

#### Stack: Python, Flask, SQLAlchemy, JWT, bcrypt, Flask-JWT-Extended

## For start in mode dev

```bash
pip install -r requirements.txt
flask run --app main.py run --debug
```

For start with gunicorn in mode prod you need to change in file `.env` DEBUG=True to DEBUG=Fasle

```bash
pip install -r requirements.txt
cd src
gunicorn main:app --bind 0.0.0.0:5000
```

For start with Docker Compose this app and PostgreSQL you need:

```bash
docker-compose up -d
```

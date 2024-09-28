#!/bin/sh


cd src

alembic upgrade head

gunicorn --config gunicorn_config.py main:app
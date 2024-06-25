#!/bin/sh
wait-for
python manage.py migrate
exec "$@"

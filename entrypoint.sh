#!/bin/bash

echo "Waiting for postgres database..."
sleep 5

echo "Apply database migrations"
python manage.py migrate

echo "Creating superuser if not exists"
python manage.py shell -c "
from django.contrib.auth import get_user_model;
User = get_user_model();
if not User.objects.filter(phone_number='${DJANGO_SUPERUSER_PHONE_NUMBER}').exists():
    User.objects.create_superuser(
        full_name='${DJANGO_SUPERUSER_FULL_NAME}', 
        phone_number='${DJANGO_SUPERUSER_PHONE_NUMBER}', 
        email='${DJANGO_SUPERUSER_EMAIL}', 
        password='${DJANGO_SUPERUSER_PASSWORD}'
    );
    print('Superuser created successfully.');
else:
    print('Superuser already exists.');
"

echo "Starting gunicorn server"
exec "$@"

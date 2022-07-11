# Heroku Specific File
release: python manage.py migrate
web: gunicorn songswipe.wsgi --preload --log-file - --timeout 10
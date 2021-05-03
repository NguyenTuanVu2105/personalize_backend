#python3 manage.py makemigrations
python3 manage.py migrate
#python3 manage.py collectstatic --noinput
#nohup celery -A HUB worker -B -l info &
if test "$DEBUG" = 'TRUE'; then
  echo "STARTING DEV SERVER"
  python3 manage.py runserver 0.0.0.0:8000
else
  echo "STARTING PRODUCTION SERVER"
  gunicorn --env DJANGO_SETTINGS_MODULE=HUB.settings --worker-class gevent --bind=0.0.0.0:8000 HUB.wsgi --workers=${NUMBER_OF_WORKERS} --timeout 300
fi

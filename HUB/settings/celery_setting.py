# CELERY STUFF
# BROKER_URL = 'redis://redis:6379'
# CELERY_RESULT_BACKEND = 'redis://redis:6379'
#
# CELERY_ACCEPT_CONTENT = ['application/json']
# CELERY_TASK_SERIALIZER = 'json'
# CELERY_RESULT_SERIALIZER = 'json'
# CELERY_TIMEZONE = 'Asia/Saigon'
import os

BROKER_URL = os.environ.get("CELERY_BROKER")
# CELERY_RESULT_BACKEND = "rpc://"
# CELERY_RESULT_BACKEND = "redis://:vantrong291@redis:6379/0"
# CELERY_RESULT_BACKEND = "db+postgresql://postgres:fulfill000@db:5432/fulfillment-hub"
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']

CELERYD_CONCURRENCY = 4
CELERYD_MAX_TASKS_PER_CHILD = 4

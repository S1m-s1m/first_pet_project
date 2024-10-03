import os
from celery import Celery
from pet_project import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pet_project.settings')

app = Celery('pet_project')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.broker_connection_retry_on_startup = True

# app.conf.broker_url = os.environ.get('REDIS_URL')  
# app.conf.result_backend = os.environ.get('REDIS_URL') 
# app.conf.task_serializer = 'json'

app.conf.broker_url = settings.CELERY_BROKER_URL
app.conf.result_backend = settings.CELERY_RESULT_BACKEND


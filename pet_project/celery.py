import sys

# import eventlet

# eventlet.monkey_patch()#Monkey patching от Eventlet заменяет эти блокирующие операции на неблокирующие, что позволяет вашим рабочим Celery обрабатывать несколько задач одновременно, повышая производительность для операций ввода-вывода

import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pet_project.settings')
app = Celery('pet_project')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.broker_connection_retry_on_startup = True

# celery -A pet_project worker -l info --pool=eventlet
# celery -A pet_project worker --loglevel=info -P eventlet
# celery -A pet_project worker --loglevel=info



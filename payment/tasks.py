from io import BytesIO
import weasyprint
from celery import shared_task
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from pet_project import settings
from order.models import Order
import logging
import time

logger = logging.getLogger(__name__)

@shared_task(name='test_task')
def test_task():
    logger.info("celery is working")
    email = EmailMessage(subject='test task', body='test task', from_email='2007kim.maksim@gmail.com', to=['2007kim.maksim@gmail.com'])
    email.send()
    return 'task performed'

@shared_task(name='payment_completed')
def payment_completed():
    email = EmailMessage(subject='payment completed', body='payment completed', from_email='2007kim.maksim@gmail.com', to=['2007kim.maksim@gmail.com'])
    email.send()
from io import BytesIO
import weasyprint
from celery import shared_task
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from pet_project import settings
from .models import Order
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

# @shared_task(name='payment_completed')
# def payment_completed(order_id):
#     """
#     Задание по отправке уведомления по электронной почте
#     при успешной оплате заказа.
#     """
#     order = Order.objects.get(pk=order_id)
#     subject = f'My Shop – Invoice no. {order.pk}'
#     message = 'Please, find attached the invoice for your recent purchase.'
#     email = EmailMessage(subject, message, '2007kim.maksim@gmail.com', [order.email])
#     # сгенерировать PDF
#     html = render_to_string('admin/orders/order/pdf.html', {'order': order})
#     out = BytesIO()
#     stylesheets=[weasyprint.CSS(settings.STATIC_ROOT / 'order/css/pdf.css')]
#     weasyprint.HTML(string=html).write_pdf(out,stylesheets=stylesheets)
#     # прикрепить PDF-файл
#     email.attach(f'order_{order.pk}.pdf',out.getvalue(),'application/pdf')
#     # отправить электронное письмо
#     email.send()

#     email = EmailMessage(subject='Good day', body='It is a second test message', from_email='2007kim.maksim@gmail.com', to=['2007kim.maksim@gmail.com'])
#     email.send()


from io import BytesIO
import weasyprint
from celery import shared_task
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from pet_project import settings
from .models import Order
import logging
import datetime

logger = logging.getLogger(__name__)

@shared_task(name='payment_completed')
def payment_completed(order_id):
    """
    Задание по отправке уведомления по электронной почте
    при успешной оплате заказа.
    """
    order = Order.objects.get(pk=order_id)
    subject = f'My Shop – Invoice no. {order.pk}'
    message = 'Please, find attached the invoice for your recent purchase.'
    email = EmailMessage(subject, message, '2007kim.maksim@gmail.com', [order.email])
    # сгенерировать PDF
    html = render_to_string('admin/orders/order/pdf.html', {'order': order})
    out = BytesIO()
    stylesheets=[weasyprint.CSS(settings.STATIC_ROOT / 'order/css/pdf.css')]
    weasyprint.HTML(string=html).write_pdf(out,stylesheets=stylesheets)
    # прикрепить PDF-файл
    email.attach(f'order_{order.pk}.pdf',out.getvalue(),'application/pdf')
    # отправить электронное письмо
    email.send()

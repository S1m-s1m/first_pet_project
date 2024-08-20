# import eventlet
#
# eventlet.monkey_patch()#Monkey patching от Eventlet заменяет эти блокирующие операции на неблокирующие, что позволяет вашим рабочим Celery обрабатывать несколько задач одновременно, повышая производительность для операций ввода-вывода


from io import BytesIO
import weasyprint
from celery import shared_task
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string

from pet_project import settings
from .models import Order
import logging

logger = logging.getLogger(__name__)

@shared_task(name='order_created')
def order_created(order_id):
    logger.info('Info message')
    order = Order.objects.get(pk=order_id)
    subject = 'Добрый день'
    message = f'Заказ был успешно оформлен, ваш номер заказа {order.pk}'
    mail_sent = send_mail(subject,
                          message,
                          '2007kim.maksim@gmail.com',
                          [order.email])
    return mail_sent

@shared_task(name='payment_completed')
def payment_completed(order_id):
    print('start payment_completed')
    """
    Задание по отправке уведомления по электронной почте
    при успешной оплате заказа.
    """
    order = Order.objects.get(pk=order_id)
    # create invoice e-mail
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

# python -m weasyprint https://weasyprint.org weasyprint.pdf
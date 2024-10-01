import stripe
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from order.models import Order
from order.tasks import payment_completed, test_task
from django.core.mail import send_mail, EmailMessage

'''
Декоратор @csrf_exempt используется для предотвращения выполнения
веб-фреймворком Django валидации CSRF, которая делается по умолчанию
для всех запросов POST. Для верификации заголовка подписи под событием 
используется метод stripe.Webhook.construct_event() библиотеки Stripe.
Если полезная нагрузка события или подпись недопустимы, то возвращается
HTTP-ответ 400 Bad Request (Неправильный запрос). В  противном случае
возвращается HTTP-ответ 200 OK. Это базовая функциональность, необходимая для 
верификации подписи и конструирования события из полезной
нагрузки JSON. Теперь можно реализовать действия конечной точки вебперехватчика
'''

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    '''
    событие (event) представляет собой действие или изменение,
    происходящее в вашем аккаунте Stripe. Это может быть, например,
    успешная оплата, отмена платежа, создание или обновление подписки и т. д.
    Когда происходит какое-либо событие в вашем аккаунте Stripe,
    Stripe генерирует уведомление (webhook) о данном событии
    и отправляет его на ваш сервер, который вы обрабатываете
    с помощью веб-перехватчика (webhook endpoint).
    Это позволяет вашему серверу реагировать на события в реальном времени,
    например, обновлять базу данных или отправлять уведомления
    '''
    try:
        event = stripe.Webhook.construct_event(
        payload,
        sig_header,
        settings.STRIPE_WEBHOOK_SECRET)
        '''
        Метод stripe.Webhook.construct_event()
        используется для проверки подписи и конструирования
        объекта события из JSON-представления события,
        полученного веб-приложением в результате входящего запроса Stripe
        '''
    except ValueError as e:
    # Недопустимая полезная нагрузка
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
    # Недопустимая подпись
        return HttpResponse(status=400)
    if event.type == 'checkout.session.completed':
        session = event.data.object
        if session.mode == 'payment' and session.payment_status == 'paid':
            try:
                order = Order.objects.get(pk=session.client_reference_id)
            except Order.DoesNotExist:
                return HttpResponse(status=404)
            # пометить заказ как оплаченный
            order.paid = True
            order.stripe_id = session.payment_intent
            order.save()# сохраняем
            # payment_completed.delay(order.pk)
            test_task.delay()
            # email = EmailMessage(subject='Good day', body='It is a test message', from_email='2007kim.maksim@gmail.com', to=['2007kim.maksim@gmail.com'])
            # email.send()
    return HttpResponse(status=200)



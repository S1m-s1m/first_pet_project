import stripe
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from order.models import Order
from order.tasks import payment_completed

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
            payment_completed.delay(order.pk)
    return HttpResponse(status=200)

'''
cd stripe_1.19.5_windows_i1386
stripe listen --forward-to 127.0.0.1:8000/payment/webhook/
это и есть endpoint но лишь в среде разработки

алгоритм работы вебхука при обработке событий Stripe:
1. **Отправка события**: Когда происходит событие в системе Stripe (например, успешная оплата или создание подписки), Stripe отправляет POST-запрос на URL вашего вебхука.
2. **Получение запроса**: Ваш веб-сервер Django принимает этот POST-запрос на URL, указанный для вебхука.
3. **Проверка подписи**: В вашем представлении вебхука сначала проверяется подпись с использованием секретного ключа, который вы установили в настройках Stripe. Это обеспечивает безопасность передаваемых данных, гарантируя, что запросы действительно отправлены Stripe и не были изменены по пути.
4. **Получение данных события**: После проверки подписи ваше приложение извлекает данные события из тела запроса. Эти данные включают в себя тип события и связанные с ним дополнительные данные, такие как идентификатор платежа или информация о заказе.
5. **Обработка события**: На основе типа события ваше приложение выполняет определенные действия. Например, если событие - успешная оплата, то ваше приложение может пометить заказ как оплаченный в базе данных или отправить уведомление покупателю.
6. **Возвращение ответа**: После успешной обработки события ваше приложение должно вернуть HTTP-ответ с кодом статуса 200 (ОК). Это сообщает Stripe, что событие было успешно обработано. Если ваше приложение вернет любой другой код статуса (например, 400 или 500), Stripe будет пытаться повторить запрос впоследствии.
7. **Логирование и обработка ошибок**: Во время обработки событий важно логировать действия вашего приложения и обрабатывать любые ошибки, которые могут возникнуть. Это помогает в отслеживании процесса обработки и устранении проблем.
'''

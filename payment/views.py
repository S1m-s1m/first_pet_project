from decimal import Decimal
import stripe
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from order.models import Order, Order_Item

# создать экземпляр Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION

def payment_process(request):
    order_pk = request.session.get('order_pk', None)
    order = get_object_or_404(Order, pk=order_pk)

    if request.method == 'POST':
        success_url = request.build_absolute_uri(reverse('payment:completed'))
        cancel_url = request.build_absolute_uri(reverse('payment:canceled'))
        # данные сеанса оформления платежа Stripe
        session_data = {
            'payment_method_types': ['card'],
            'mode': 'payment',
            'client_reference_id': order.pk,
            'success_url': success_url,
            'cancel_url': cancel_url,
            'line_items': []
        }
        # добавить товарные позиции заказа
        # в сеанс оформления платежа Stripe
        for item in Order_Item.objects.filter(order=order):
            session_data['line_items'].append({
                'price_data': {
                    'unit_amount': int(item.price * Decimal('100')),
                    'currency': 'usd',
                    'product_data': {
                        'name': item.product.name,
                        },
                    },
                'quantity': item.quantity,
            })

            # купон Stripe
        if order.coupon:
            stripe_coupon = stripe.Coupon.create(
                name=order.coupon.code,
                percent_off=order.discount,
                duration='once')
            session_data['discounts'] = [{
                'coupon': stripe_coupon.id
            }]

        # создать сеанс оформления платежа Stripe
        session = stripe.checkout.Session.create(**session_data)
        # перенаправить к платежной форме Stripe
        # return redirect(session.url, code=303)
        return redirect(session.url)
    else:
        return render(request, 'payment/process.html', locals())# locals - context с парами ключ=значение

def payment_completed(request):
    return render(request, 'payment/completed.html')

def payment_canceled(request):
    return render(request, 'payment/canceled.html')


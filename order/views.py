import os

os.add_dll_directory(r"C:\Program Files (x86)\gtk-3.8.1")
import weasyprint
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.views import View
from django.utils.translation import gettext_lazy as _
from cart.cart_session import Cart
from catalog.recommender import Recommender
from order.forms import OrderForm
from pet_project import settings
from .models import Order_Item, Order

# Create your views here.

class Order_History(View):
    def get(self, request):
        objects = Order.objects.filter(user=request.user)
        return render(request, 'order/order_history.html', {'objects':objects})

class Create_Order(View):
    def get(self, request):
        form = OrderForm()
        return render(request, 'order/order_create.html', {'form': form})

    def post(self, request):
        cart = Cart(request)
        if cart:
            form = OrderForm(request.POST)
            if form.is_valid():
                order = form.save(commit=False)
                order.user = request.user
                # order = form.save(commit=False)
                if cart.coupon:
                    order.coupon = cart.coupon
                    order.discount = cart.coupon.discount
                order.save()
                for item in cart:
                    Order_Item.objects.create(order=order,
                                             product=item['product'],
                                             price=item['price'],
                                             quantity=item['quantity'])
                # очистка корзины
                cart.clear()

                # Update Redis with purchased products
                r = Recommender()
                products_in_order = [item['product'] for item in cart]
                r.products_bought(products_in_order)

                # order_detail.delay(order.pk)
                # order_created.delay(order.pk)

                request.session['order_pk'] = order.pk
                # order_cost = order.total_order_cost()
                # перенаправить к платежу
                # return redirect(reverse('payment:process'))
                return render(request, 'payment/process.html', {'order': order})
        else:
            error = _('Yor cart is empty')
            return render(request, 'order/error_page.html', {'error': error})

class Order_Detail(View):
    def get(self, request, pk):
        try:
            order = Order.objects.get(pk=pk)
            return render(request, 'order/order_detail.html', {'object': order})
        except  Order.DoesNotExist:
            error = _('There is no such product')
            return render(request, 'order/error_page.html', {'error':error})

@staff_member_required
def admin_order_detail(request, pk):
    try:
        order = Order.objects.get(pk=pk)
        return render(request,'admin/orders/order/detail.html',{'order': order})
    except  Order.DoesNotExist:
        error = _('There is no such product')
        return render(request, 'order/error_page.html', {'error': error})

@staff_member_required
def admin_order_pdf(request, pk):
    order = get_object_or_404(Order, pk=pk)
    html = render_to_string('admin/orders/order/pdf.html', {'order': order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{order.pk}.pdf'
    stylesheets=[weasyprint.CSS(settings.STATIC_ROOT / 'order/css/pdf.css')]
    weasyprint.HTML(string=html).write_pdf(response,stylesheets=stylesheets)
    return response


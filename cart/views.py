from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.decorators.http import require_POST
from django.utils.translation import gettext_lazy as _
from cart.cart_session import Cart
from cart.forms import CartAddProductForm
from catalog.models import Product
from catalog.recommender import Recommender
from coupon.forms import CouponApplyForm


# Create your views here.

# class Cart_View(View):
#     def get(self, request):
#         cart_items = Cart.objects.filter(user=request.user)
#         total_price = sum(item.product.price * item.quantity for item in cart_items)
#         return render(request, 'cart/cart_view.html', {'cart_items':cart_items, 'total_price': total_price})
#
#
# class Add_To_Cart(View):
#     def get(self, request, pk):
#         try:
#             product = Product.objects.get(pk=pk)
#             cart_object, status = Cart.objects.get_or_create(product=product, user=request.user)# get_or_create в первой переменной возвращает объект(новый или полученный) а во второй логическое значение, указывающее, был ли объект только что создан
#             if status:
#                 cart_object.quantity = 1
#             else:
#                 cart_object.quantity += 1
#             cart_object.save()
#             return redirect('cart:cart_view')
#         except Product.DoesNotExist:
#             error = 'Такого товара не существует'
#             return render(request, 'cart/error_page.html', {'error':error})
#
# class Add_One(View):
#     def get(self, request, pk):
#         product = Product.objects.get(pk=pk)
#         cart_object = Cart.objects.get(product=product, user=request.user)
#         cart_object.quantity += 1
#         cart_object.save()
#         return redirect('cart:cart_view')
#
# class Sub_One(View):
#     def get(self, request, pk):
#         product = Product.objects.get(pk=pk)
#         cart_object = Cart.objects.get(product=product, user=request.user)
#         if cart_object.quantity > 0:
#             cart_object.quantity -= 1
#         else:
#             cart_object.quantity = 0
#         cart_object.save()
#         return redirect('cart:cart_view')
#
# class Remove_From_Cart(View):
#     def get(self, request, pk):
#         object = Cart.objects.get(pk=pk)
#         object.delete()
#         return redirect('cart:cart_view')

@require_POST
def cart_add(request, pk):
    cart = Cart(request)
    try:
        product = Product.objects.get(pk=pk)
        form = CartAddProductForm(request.POST)
        if form.is_valid():
            cart.add(product=product,
                     quantity=form.cleaned_data['quantity'],
                     update_quantity=form.cleaned_data['update'])
        return redirect('cart:cart_detail')
    except Product.DoesNotExist:
        error = _('There is no such product')
        return render(request, 'cart/error_page.html', {'error':error})

def cart_remove(request, pk):
    cart = Cart(request)
    try:
        product = Product.objects.get(pk=pk)
        cart.remove(product)
        return redirect('cart:cart_detail')
    except Product.DoesNotExist:
        error = _('There is no such product')
        return render(request, 'cart/error_page.html', {'error':error})

def cart_detail(request):
    cart = Cart(request)
    coupon_apply_form = CouponApplyForm()
    r = Recommender()
    cart_products = [item['product'] for item in cart]
    if (cart_products):
        recommended_products = r.suggest_products_for(cart_products, max_results=4)
    else:
        recommended_products = []
    context = {'cart': cart, 'coupon_apply_form': coupon_apply_form, 'recommended_products': recommended_products}
    return render(request, 'cart/cart_detail.html', context)

def cart_add_one(request, pk):
    cart = Cart(request)
    try:
        product = Product.objects.get(pk=pk)
        cart.add_one(product)
        return redirect('cart:cart_detail')
    except Product.DoesNotExist:
        error = _('There is no such product')
        return render(request, 'cart/error_page.html', {'error':error})

def cart_remove_one(request, pk):
    cart = Cart(request)
    try:
        product = Product.objects.get(pk=pk)
        cart.remove_one(product)
        return redirect('cart:cart_detail')
    except Product.DoesNotExist:
        error = _('There is no such product')
        return render(request, 'cart/error_page.html', {'error':error})

def clear_cart(request):
    cart = Cart(request)
    cart.clear()
    return redirect('cart:cart_detail')

#изменить логику cart, для сессий не нужна модель, изменить все шаблоны и пути к ним в редиректах   рендерах в том числе
#платежная система по книге, но джанго по умолчанию создаст таблицу django_session для хранений сессий


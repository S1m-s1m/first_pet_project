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


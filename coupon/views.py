from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.contrib import messages
from cart.cart_session import Cart
from catalog.recommender import Recommender
from coupon.forms import CouponApplyForm
from coupon.models import Coupon
from django.utils.translation import gettext_lazy as _

# Create your views here.
# @require_POST
# def coupon_apply(request):
#     now = timezone.now()
#     form = CouponApplyForm(request.POST)
#     if form.is_valid():
#         code = form.cleaned_data['code']
#         try:
#             coupon = Coupon.objects.get(code__iexact=code,
#                                         valid_from__lte=now,
#                                         valid_to__gte=now,
#                                         active=True)
#             request.session['coupon_id'] = coupon.id
#         except Coupon.DoesNotExists:
#             request.session['coupon_id'] = None
#     return redirect('cart:cart_detail')

@require_POST
def coupon_apply(request):
    now = timezone.now()
    form = CouponApplyForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            coupon = Coupon.objects.get(code__iexact=code,
                                        valid_from__lte=now,
                                        valid_to__gte=now,
                                        active=True)
            if coupon.used_count < coupon.max_uses:
                # Allow the coupon to be applied
                request.session['coupon_id'] = coupon.pk
                # Increment the used count
                coupon.used_count += 1
                coupon.save()
            else:
                # Coupon usage limit reached
                request.session['coupon_id'] = None
                form.add_error(None, _('This coupon has been used the maximum number of times'))
                # messages.success(request, _('This coupon has been used the maximum number of times'))
                '''
                messages.success(request, message) is a function 
                in Django that adds a success message to the current 
                user's session. When a user performs an action, such as 
                submitting a form or completing a task, you can call 
                messages.success() to provide feedback to the user that 
                the action was successful. This message will be stored 
                temporarily in the user's session and will be available 
                to be displayed on the next page they visit. It's commonly 
                used in conjunction with a redirect to show a success 
                message on the next page
                
                messages.success(request, message): 
                Adds a success message to the current user's session. 
                It's typically used to inform the user that an action 
                was successfully completed.

                messages.error(request, message): 
                Adds an error message to the current user's session. 
                It's used to inform the user about errors or problems 
                that occurred during an action.

                messages.warning(request, message): 
                Adds a warning message to the current user's session. 
                It's used to alert the user about potential issues or 
                situations that require attention.

                messages.info(request, message): 
                Adds an informational message to the current user's session. 
                It's used to provide general information to the user 
                that may be helpful or relevant.
                '''
        except Coupon.DoesNotExist:
            request.session['coupon_id'] = None
            messages.success(request, _('This coupon does not exist or is not valid'))
    return redirect('cart:cart_detail')


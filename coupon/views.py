from django.shortcuts import redirect
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.contrib import messages
from coupon.forms import CouponApplyForm
from coupon.models import Coupon
from django.utils.translation import gettext_lazy as _


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
                request.session['coupon_id'] = coupon.pk
                coupon.used_count += 1
                coupon.save()
            else:
                request.session['coupon_id'] = None
                form.add_error(None, _('This coupon has been used the maximum number of times'))
        except Coupon.DoesNotExist:
            request.session['coupon_id'] = None
            messages.success(request, _('This coupon does not exist or is not valid'))
    return redirect('cart:cart_detail')


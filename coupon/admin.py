from django.contrib import admin
from coupon.models import Coupon


# Register your models here.
class CouponAdmin(admin.ModelAdmin):
    list_display = ['pk', 'code', 'valid_from', 'valid_to', 'discount', 'active', 'max_uses', 'used_count']
    list_filter = ['active', 'valid_from', 'valid_to']
    search_fields = ['code']
admin.site.register(Coupon, CouponAdmin)
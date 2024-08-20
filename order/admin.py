import csv
import datetime
from django.contrib import admin
from django.http import HttpResponse
from django.urls import reverse
from django.utils.safestring import mark_safe
from order.models import Order_Item, Order

# Register your models here.

def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename={}.csv'.format(opts.verbose_name)
    writer = csv.writer(response)
    fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]
    # Write a first row with header information
    writer.writerow([field.verbose_name for field in fields])
    # Write data rows
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response

export_to_csv.short_description = 'Export to CSV'

class OrderItemInline(admin.TabularInline):
    model = Order_Item
    raw_id_fields = ['product']

def order_detail(obj):
    url = reverse('order:admin_order_detail', kwargs={'pk': obj.pk})
    return mark_safe(f'<a href="{url}">View</a>')

def order_stripe_payment(obj):
    url = obj.get_stripe_url()
    if obj.stripe_id:
        html = f'<a href="{url}" target="_blank">{obj.stripe_id}</a>'
        return mark_safe(html)
    return ''

order_stripe_payment.short_description = 'Stripe payment'

def order_pdf(obj):
    url = reverse('order:admin_order_pdf', args=[obj.id])
    return mark_safe(f'<a href="{url}">PDF</a>')

order_pdf.short_description = 'Invoice'

class OrderAdmin(admin.ModelAdmin):
    list_display = ['pk', 'first_name', 'last_name', 'email',
                    'address', 'user', 'city', 'paid', 'coupon', 'discount', 'created',
                    order_detail, order_pdf, order_stripe_payment]
    list_filter = ['paid', 'created']
    list_display_links = ['user', 'coupon']
    inlines = [OrderItemInline]
    actions = [export_to_csv]

class Order_ItemAdmin(admin.ModelAdmin):
    list_display = ['pk', 'product', 'quantity', 'order', 'price']
    list_filter = ['price']
    list_display_links = ['product', 'order']

admin.site.register(Order, OrderAdmin)
admin.site.register(Order_Item, Order_ItemAdmin)


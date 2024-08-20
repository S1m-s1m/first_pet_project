
from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import Category, Product, Brand, Review
from parler.admin import TranslatableAdmin

# class BrandAdmin(admin.ModelAdmin):
#     list_display = ['name', 'description', 'image']
#     list_filter = ['id']
#
# class ProductAdmin(admin.ModelAdmin):
#     list_display = ['name', 'description', 'category', 'price', 'brand', 'size', 'image', 'availability', 'created']
#     list_filter = ['availability', 'created', 'brand']

class BrandAdmin(TranslatableAdmin):
    list_display = ['pk', 'name', 'slug', 'description']
    list_display_links = ['slug', 'name']

    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ('name',)}

class CategoryAdmin(TranslatableAdmin):
    list_display = ['pk', 'slug', 'name']
    list_display_links = ['slug', 'name']

    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ('name',)}

class ProductAdmin(TranslatableAdmin):
    list_display = ['pk', 'name', 'slug', 'category', 'brand', 'price', 'availability', 'created', 'size', 'image', 'description']
    list_display_links = ['slug', 'name']
    list_filter = ['availability', 'created']
    list_editable = ['price', 'availability']

    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ('name',)}

class ReviewAdmin(ModelAdmin):
    list_display = ['pk', 'product', 'author', 'date', 'parent']
    list_display_links = ['pk']

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Review, ReviewAdmin)
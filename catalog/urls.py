from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from catalog.views import Create_Brand, Product_Catalog, Update_Product, Update_Brand, \
    Brand_List, Brand_Detail, Delete_Product, Delete_Brand, Product_Detail, Create_Category, Delete_Category, \
    Create_Product, Translate_Category, Delete_Review

app_name = 'catalog'

urlpatterns = [
    path('', Product_Catalog.as_view(), name='catalog_view'),
    path('delete_review/<int:pk>/', Delete_Review.as_view(), name='delete_review'),
    path('create_product/', Create_Product.as_view(), name='create_product'),
    path('detail_product/<int:pk>/<str:slug>/', Product_Detail.as_view(), name='product_detail'),
    path('update_product/<int:pk>/', Update_Product.as_view(), name='update_product'),
    path('delete_product/<int:pk>/', Delete_Product.as_view(), name='delete_product'),

    path('brand_list/', Brand_List.as_view(), name='brand_list'),
    path('create_brand/', Create_Brand.as_view(), name='create_brand'),
    path('detail_brand/<int:pk>/', Brand_Detail.as_view(), name='brand_detail'),
    path('update_brand/<int:pk>/', Update_Brand.as_view(), name='update_brand'),
    path('delete_brand/<int:pk>/', Delete_Brand.as_view(), name='delete_brand'),

    path('create_category/', Create_Category.as_view(), name='create_category'),
    path('delete_category/<int:pk>/', Delete_Category.as_view(), name='delete_category'),
    path('translate_category/<int:pk>/', Translate_Category.as_view(), name='translate_category'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
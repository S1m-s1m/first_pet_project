"""
URL configuration for pet_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.i18n import i18n_patterns

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path(r'', include("main_app.urls", namespace='main_app')),
#     path('catalog/', include("catalog.urls", namespace='catalog')),
#     path('cart/', include("cart.urls", namespace='cart')),
#     path('order/', include("order.urls", namespace='order')),
#     path('coupon/', include('coupon.urls', namespace='coupon')),
#     path('rosetta/', include('rosetta.urls')),
# ]

urlpatterns = i18n_patterns(
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^', include("main_app.urls", namespace='main_app')),
    re_path(r'^catalog/', include("catalog.urls", namespace='catalog')),
    re_path(r'^cart/', include("cart.urls", namespace='cart')),
    re_path(r'^order/', include("order.urls", namespace='order')),
    re_path(r'^coupon/', include('coupon.urls', namespace='coupon')),
    re_path(r'^rosetta/', include('rosetta.urls')),
)

urlpatterns += [
    path('payment/', include('payment.urls', namespace='payment'))
]# отдельно чтобы не было в i18n_patterns
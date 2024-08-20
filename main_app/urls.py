from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path

from main_app.views import main, register_view, login_view, logout_view, profile

app_name = 'main_app'

urlpatterns = [
    path('', main, name='main'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile, name='profile'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
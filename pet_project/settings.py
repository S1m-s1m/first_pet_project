"""
Django settings for pet_project project.

Generated by 'django-admin startproject' using Django 5.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
import os
from pathlib import Path
from dotenv import load_dotenv
from django.utils.translation import gettext_lazy as _
import dj_database_url
import logging

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-mc9grg_heu12t^!s3f=-4*q#v+9c)364$&fff*9@9+3!_vdr3i'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

#ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'tunnel1-tunnelinuser489.p.tnnl.in', '0.0.0.0']
# ALLOWED_HOSTS = ["first-pet-project-1.onrender.com", "tunnel1-tunnelinuser489.p.tnnl.in", 'localhost', '127.0.0.1', "0.0.0.0"]
ALLOWED_HOSTS = ["firstpetproject-production.up.railway.app", "tunnel1-tunnelinuser489.p.tnnl.in", 'localhost', '127.0.0.1', "0.0.0.0"]
CSRF_TRUSTED_ORIGINS = ["https://tunnel1-tunnelinuser489.p.tnnl.in", "https://first-pet-project-1.onrender.com", "https://firstpetproject-production.up.railway.app"]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'main_app',
    'catalog',
    'cart',
    'order',
    'coupon',
    'rest_framework',
    'parler',
    'rosetta',
    'payment.apps.PaymentConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'pet_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'pet_project.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

load_dotenv()

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': os.environ.get('DB_NAME'),
#         'USER': os.environ.get('DB_USER'),
#         'PASSWORD': os.environ.get('DB_PASSWORD'),
#         # 'HOST': 'localhost',
#         'HOST': os.environ.get('DB_HOST'),
#         'PORT': '5432',
#         'TEST': {
#             'NAME': 'test_online_shop',
#         },
#     }
# }

DATABASES = {
    'default': dj_database_url.parse(os.environ.get('DATABASE_URL')),
    'TEST': {
        'NAME': 'test_online_shop',
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

STATIC_ROOT = BASE_DIR / 'static'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'catalog', 'static'),
    os.path.join(BASE_DIR, 'order', 'static'),
    os.path.join(BASE_DIR, 'coupon', 'static'),
    os.path.join(BASE_DIR, 'main_app', 'static'),
    os.path.join(BASE_DIR, 'payment', 'static'),
    os.path.join(BASE_DIR, 'cart', 'static'),
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'main_app.User'

CART_SESSION_ID = 'cart'

# CELERY_BROKER_URL = 'redis://localhost:6379/0'  
# CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
# CELERY_BROKER_URL = 'redis://redis:6379/0'  # URL Redis для брокера сообщений
# CELERY_RESULT_BACKEND = 'redis://redis:6379/0'  # URL Redis для хранения результатов задач
CELERY_BROKER_URL = os.environ.get('REDIS_URL')  # URL Redis для брокера сообщений
CELERY_RESULT_BACKEND = os.environ.get('REDIS_URL')
CELERY_ACCEPT_CONTENT = ['application/json']  # Форматы контента, которые Celery может принимать
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    },
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS') == 'True'
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')

#REDIS_HOST = 'localhost'
# REDIS_HOST = 'redis'
# REDIS_URL = 'redis://localhost:6379/0'
REDIS_HOST = os.environ.get('REDIS_HOST')
REDIS_URL = os.environ.get('REDIS_URL')
REDIS_PORT = 6379
REDIS_DB = 1

LANGUAGES = (
    ('en', _('English')),
    ('ru', _('Russian')),
)

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale/'),
)

PARLER_LANGUAGES = {
    None: (
        {'code': 'en'},
        {'code': 'ru'},
    ),
    'default': {
        'fallback': 'en',
        'hide_untranslated': False,
    }
}

STRIPE_PUBLISHABLE_KEY = 'pk_test_51PLAVyDo5uaPJl4sZnu2nfKjDPjFQqgc24tfaMw4JnE0QsaVxRJ7tWiaUKpnFduAPfQbJpzr7Mge1d2wkNocl1hU00YSQk285H'
STRIPE_SECRET_KEY = 'sk_test_51PLAVyDo5uaPJl4svwhpMCwmcRdLWVQjKmNm8ddxkxBh1ZrJtMDXqeQDpmeuuU2QPrONZurEjF6V3djGWlsT6mjc00pIB7NZLp'
STRIPE_API_VERSION = '2024-04-10'
STRIPE_WEBHOOK_SECRET = 'whsec_1OKFmYuMZuQL0t9Egu5YfYhZwgWyv6hM'
# STRIPE_WEBHOOK_SECRET = 'whsec_o4MTEkPB8tYpojzDIz8Llk7X47dOG4iw'
#STRIPE_WEBHOOK_SECRET = 'whsec_KzYJyda8cJe61FKMB9dVGDo8340Ab27z'
#STRIPE_WEBHOOK_SECRET = 'whsec_13cd44143fc8bb61ae9f21b48ae61b975ebf30d8eec5cf49a9d407144d74d27b'

# STRIPE_PUBLISHABLE_KEY = os.environ.get('STRIPE_PUBLISHABLE_KEY')
# STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY')
# STRIPE_API_VERSION = os.environ.get('STRIPE_API_VERSION')
# STRIPE_WEBHOOK_SECRET = os.environ.get('STRIPE_WEBHOOK_SECRET')


#set PATH=%PATH%;%SystemRoot%\system32;C:\Users\Максим\Downloads\gettext\bin

# django-admin makemessages --all внесение слов
# makemessages: Эта команда создает файлы перевода
# .po для всех текстовых строк, помеченных для перевода
# в коде вашего Django приложения. Она анализирует
# исходный код приложения, находит все строки,
# которые должны быть переведены, и создает
# соответствующие файлы .po или слова для перевода

# django-admin compilemessages применение перевода слов
# Эта команда компилирует файлы перевода .po
# в бинарные файлы формата .mo, которые Django
# может использовать для перевода текста на другие языки.
# Это необходимо для того, чтобы Django мог
# эффективно загружать и использовать переводы
# во время выполнения. Команда обычно вызывается после того,
# как были внесены или изменены переводы,
# чтобы обновить бинарные файлы перевода.


# python -m weasyprint https://weasyprint.org weasyprint.pdf


# celery -A pet_project worker -l info --pool=eventlet
# celery -A pet_project worker --loglevel=info -P eventlet


# cd stripe_1.21.0_windows_x86_64
# stripe listen --forward-to 127.0.0.1:8000/payment/webhook/
# это и есть endpoint но лишь в среде разработки

# алгоритм работы вебхука при обработке событий Stripe:
# 1. **Отправка события**: Когда происходит событие в системе Stripe (например, успешная оплата или создание подписки), Stripe отправляет POST-запрос на URL вашего вебхука.
# 2. **Получение запроса**: Ваш веб-сервер Django принимает этот POST-запрос на URL, указанный для вебхука.
# 3. **Проверка подписи**: В вашем представлении вебхука сначала проверяется подпись с использованием секретного ключа, который вы установили в настройках Stripe. Это обеспечивает безопасность передаваемых данных, гарантируя, что запросы действительно отправлены Stripe и не были изменены по пути.
# 4. **Получение данных события**: После проверки подписи ваше приложение извлекает данные события из тела запроса. Эти данные включают в себя тип события и связанные с ним дополнительные данные, такие как идентификатор платежа или информация о заказе.
# 5. **Обработка события**: На основе типа события ваше приложение выполняет определенные действия. Например, если событие - успешная оплата, то ваше приложение может пометить заказ как оплаченный в базе данных или отправить уведомление покупателю.
# 6. **Возвращение ответа**: После успешной обработки события ваше приложение должно вернуть HTTP-ответ с кодом статуса 200 (ОК). Это сообщает Stripe, что событие было успешно обработано. Если ваше приложение вернет любой другой код статуса (например, 400 или 500), Stripe будет пытаться повторить запрос впоследствии.
# 7. **Логирование и обработка ошибок**: Во время обработки событий важно логировать действия вашего приложения и обрабатывать любые ошибки, которые могут возникнуть. Это помогает в отслеживании процесса обработки и устранении проблем.

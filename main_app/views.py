from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from main_app.forms import UserForm, LoginForm, ProfileForm
from django.utils.translation import gettext_lazy as _
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test

# Create your views here.

'''интернет магазин с обработкой задач через селери, модeли: User, Products, Orders
реализация корзины, комментариев, тесты, поисковой строки, пайплайн'''

'''добавить профиль и возможность его изменения'''

def is_authenticated(user):
    return user.is_authenticated

def main(request):
    return render(request, 'main_app/main.html', {'request': request})

def register_view(request):
    if request.method == 'POST':
        form = UserForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            user = authenticate(request=request, email=email, password=password)
            if user:
                login(request, user=user)
                return redirect('main_app:main')
        else:
            return render(request, 'main_app/login_form.html', {'form': form, 'form_name': _('Register form')})
    else:
        return render(request, 'main_app/login_form.html', {'form': UserForm(), 'form_name': _('Register form')})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request=request, email=email, password=password)
            if user:
                login(request, user)
                return redirect('main_app:main')
            # else:# не нужно так как authenticate при не нахождении пользователя определит форму не валидной
            #     form.add_error(None, 'User was not found')
            else:# нужно т.к мы используем обычную форму а не AuthenticationForm
                form.add_error(None, _('User was not found'))
                return render(request, 'main_app/login_form.html', {'form': form, 'form_name': _('Authentication form')})
        else:
            form.add_error(None, _('Form data is invalid'))
            return render(request, 'main_app/login_form.html', {'form': form, 'form_name': _('Authentication form')})
    else:
        form = LoginForm()
        return render(request, 'main_app/login_form.html', {'form': form, 'form_name': _('Authentication form')})

@user_passes_test(is_authenticated)
def logout_view(request):
    logout(request)
    return redirect('main_app:main')

@user_passes_test(is_authenticated)
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(data=request.POST, files=request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('main_app:main')
        else:
            return render(request, 'main_app/profile.html', {'form': form})
    else:
        form = ProfileForm(instance=request.user)
        return render(request, 'main_app/profile.html', {'form': form})



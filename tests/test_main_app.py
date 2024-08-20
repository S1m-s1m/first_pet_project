from django.contrib.auth import get_user_model
import pytest
from django.urls import reverse
from main_app.forms import UserForm, LoginForm, ProfileForm

pytestmark = pytest.mark.django_db

User = get_user_model()

class TestRegisterView:

    def test_get_register_view(self, client):
        url = reverse('main_app:register')
        response = client.get(path=url)
        assert response.status_code == 200
        assert isinstance(response.context['form'], UserForm)

    def test_post_register_view(self, client):
        url = reverse('main_app:register')
        data = {
            'email': 'test_user@gmail.com',
            'password1': 'test_password',
            'password2': 'test_password',
            'username': 'test_user',
            'first_name': 'test_first_name',
            'last_name': 'test_last_name'
        }
        response = client.post(path=url, data=data)
        user = User.objects.get(email='test_user@gmail.com')
        assert response.status_code == 302
        assert User.objects.filter(email='test_user@gmail.com').exists()
        assert int(client.session['_auth_user_id']) == user.pk

class TestLoginView:

    def test_get_login_view(self, client):
        url = reverse("main_app:login")
        response = client.get(path=url)
        assert response.status_code == 200
        assert isinstance(response.context['form'], LoginForm)

    def test_post_login_view(self, client, user):
        url = reverse("main_app:login")
        data = {
            'email': 'user@gmail.com',
            'password': 'password'
        }
        response = client.post(path=url, data=data)
        assert User.objects.filter(email='user@gmail.com').exists() == True
        assert response.status_code == 302
        assert int(client.session['_auth_user_id']) == user.pk

class TestLogoutView:

    def test_get_logout_view(self, client, user):
        client.login(email='user@gmail.com', password='password')
        url = reverse('main_app:logout')
        response = client.get(path=url)
        assert response.status_code == 302
        assert '_auth_user_id' not in client.session

class TestProfileView:

    def test_get_profile_view(self, client, user):
        client.login(email='user@gmail.com', password='password')
        url = reverse('main_app:profile')
        response = client.get(path=url)
        assert response.status_code == 200
        assert isinstance(response.context['form'], ProfileForm)

    def test_post_profile_test(self, client, user):
        client.login(email='user@gmail.com', password='password')
        url = reverse('main_app:profile')
        data = {
            'username': 'new username',
            'first_name': 'new first name',
            'last_name': 'new last name'
        }
        response = client.post(path=url, data=data)
        assert response.status_code == 302
        redirect_url = response['Location']
        expected_url = reverse('main_app:main')
        assert redirect_url == expected_url
        user.refresh_from_db()
        assert user.username == 'new username'

'''разобраться с ошибкой редис'''
#pytest tests/test_main_app.py
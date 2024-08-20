from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils.translation import gettext_lazy as _
from main_app.models import User

class UserForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(), max_length=100, label=_('password1'))
    password2 = forms.CharField(widget=forms.PasswordInput(), max_length=100, label=_('password2'))

    def check_password(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 == password2:
            return password1
        else:
            raise forms.ValidationError("Passwords do not match")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        else:
            return user

    def clean_username(self):
        # Просто возвращаем значение без проведения проверки уникальности
        return self.cleaned_data['username']

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email', 'first_name', 'last_name', 'avatar',)

class LoginForm(forms.Form):
    email = forms.EmailField(label=_('email'))
    password = forms.CharField(max_length=100, widget=forms.PasswordInput(), label=_('password'))

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'avatar',)
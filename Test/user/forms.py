from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import AbstractUser


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = AbstractUser
        fields = ["account", "email", "phone", "password1", "password2"]

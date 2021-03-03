from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from user.models import User


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'password1', 'password2', 'first_name', 'last_name', 'mobile_phone']
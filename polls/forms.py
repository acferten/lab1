from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError
from polls.models import AdvUser


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = AdvUser
        fields = ['username', 'password1', 'password2', 'avatar']

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','phone', 'email', 'password1', 'password2','is_theatre_manager']
        


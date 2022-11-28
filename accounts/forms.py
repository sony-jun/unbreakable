from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ["username","fullname","birthday","phone_number"]
        labels =  {
            'username':'ID',
            'fullname':'성함',
            'birthday':'생년월일',
            'phone_number':'전화번호',
        }
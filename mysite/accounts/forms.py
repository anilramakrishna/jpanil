from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
class orderform(ModelForm):
    class Meta:
        model=Order
        fields='__all__'

class oderform1(ModelForm):
    class Meta:
        model=Order
        fields=['status']

class createuserform(UserCreationForm):
    class Meta:
        model=User
        fields=['username','email','password1','password2']
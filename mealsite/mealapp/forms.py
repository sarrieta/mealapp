from django import forms
import re
from django.forms import ModelChoiceField
from django.db import models
from .models import*
from .forms import *



class Rental(forms.ModelForm):
    class Meta:
        model = Rental
        fields = ['address','geolocation']

class UserLogInForm(forms.Form):
    username = forms.CharField( min_length=2,max_length=15, widget=forms.TextInput(attrs={
        'placeholder':'Username',
        'id':'id_log_username'
        }))
    password = forms.CharField( min_length=1,max_length=32, widget=forms.PasswordInput(attrs={
        'placeholder':'Password',
        'id':'id_log_password'
        }))

class UserRegForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['username','password','preferences']
        labels = {
            }
        widgets = {
            'username':forms.TextInput(attrs={"placeholder":"Enter username"}),
            'password': forms.PasswordInput(attrs={"placeholder":"Enter password"}),

           }
    re_password = forms.CharField(label='Repeat Password',max_length=32, widget=forms.PasswordInput(attrs={
    "placeholder":"Repeat password",
    "name":"re_password"}))



class PreferencesForm(forms.ModelForm):
    class Meta:
        model = Preferences
        fields = ['preferences']

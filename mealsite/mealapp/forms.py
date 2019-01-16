from django import forms
import re
from django.forms import ModelChoiceField
from django.db import models
from .models import*
from .forms import *

class UserLogInForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['username','password']

    widgets = {
        'password': forms.PasswordInput(),

       }

class UserRegForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['username','password','preferences']
        labels = {
            }
        widgets = {
            'password': forms.PasswordInput(),
            'preferences':forms.Textarea(attrs={'rows':5, 'cols':20, 'readonly':'readonly'})
           }


class PreferencesForm(forms.ModelForm):
    class Meta:
        model = Preferences
        fields = ['preferences']

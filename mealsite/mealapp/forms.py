from django import forms
import re
from django.forms import ModelChoiceField
from django.db import models
from .models import*
from django.core.validators import validate_email
from django.core.exceptions import ValidationError



class UserRegForm(forms.Form):


    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={
    "placeholder":"Username",
    "pattern":"[[^A-Za-z0-9]{3,15}",
    "name":"username",
    "title":"Usernames must be between 3 and 15 characters. Only letters and numbers are allowed"
    }))

    password = forms.CharField(label='Password',max_length=32, widget=forms.PasswordInput(attrs={
    "placeholder":"Enter password",
    "pattern":"(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}",
    "name":"password",
    "title":"Password must contain at least one number and one uppercase and lowercase letter, and at least 8 or more characters"
    }))
    re_password = forms.CharField(label='Repeat Password',max_length=32, widget=forms.PasswordInput(attrs={
    "placeholder":"Repeat password",
    "name":"re_password"}))






class UserLogInForm(forms.Form):
        username = forms.CharField( min_length=2,max_length=15, widget=forms.TextInput(attrs={
        'placeholder':'Username',
        'class':'form-control',
        'id':'id_log_username'
        }))
        password = forms.CharField( min_length=8,max_length=32, widget=forms.PasswordInput(attrs={
        'placeholder':'Password',
        'class':'form-control',
        'id':'id_log_password'
        }))



class UserProfile(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['email','dob','number','gender']
        labels = {
                "number": "Number*"
            }

        widgets = {
            'email': forms.TextInput(attrs={
                'placeholder': 'Email',
                'pattern':'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)',
                'class':'input',
                }),

            'dob': forms.DateInput(attrs={
            'placeholder': 'Date of Birth',
            'class':'input',
            'readonly':'true'

            }),

            'number': forms.TextInput(attrs={
                'placeholder': 'Phone number',
                'class':'input',
                'required':'true',
                'pattern':'^(\+44\s?7\d{3}|\(?07\d{3}\)?)\s?\d{3}\s?\d{3}$',
                'title':'UK mobile phone number, with optional +44 national code. Allows optional brackets and spaces at appropriate positions.'
                }),







        }



class MemberProfile(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['hobbies']
        widgets={


            }

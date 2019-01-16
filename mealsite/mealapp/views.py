from django.shortcuts import render
from django.http import HttpResponse

# Scraper imports
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
from .models import Menu
from .forms import *



def index(request):

	return render (request,'index.html')

def map(request):

	return render (request,'map.html')

def login(request):
	login_form = UserLogInForm()
	return render (request,'login.html',{'login_form': login_form})

def register(request):
	reg_form = UserRegForm()

	return render (request,'register.html',{'reg_form': reg_form})

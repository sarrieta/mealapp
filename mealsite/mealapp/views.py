from django.shortcuts import render
from django.http import HttpResponse

# Scraper imports
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
from .models import Menu




def index(request):

	return render (request,'index.html')

def map(request):

	return render (request,'map.html')

def login(request):

	return render (request,'login.html')

def register(request):

	return render (request,'register.html')

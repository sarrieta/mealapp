from django.shortcuts import render
from django.http import HttpResponse

# Scraper imports
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
from .models import Menu


def index(request):


	return render (request,'index.html')


def search(request):

	return render (request,'search.html')

def search2(request):
	#return HttpResponse("Hello you are at the index")
	return render (request,'search2.html')

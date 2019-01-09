from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def index(request):
	#return HttpResponse("Hello you are at the index")
	return render (request,'index.html')


def search(request):
	#return HttpResponse("Hello you are at the index")
	return render (request,'search.html')

def search2(request):
	#return HttpResponse("Hello you are at the index")
	return render (request,'search2.html')

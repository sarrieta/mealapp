from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.http import JsonResponse
import json
from django.core import serializers

#geocoding imports
import googlemaps
from datetime import datetime
gmaps = googlemaps.Client(key='AIzaSyCpFC94xiuIL1vHEBiGv43sgVga7aJTA1c')
# Scraper imports
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
from .models import *
from .forms import *

#ML imports#
import json
import re
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, accuracy_score
from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import make_pipeline, make_union
from itertools import chain
from sklearn.linear_model import LogisticRegression
from nltk.stem import WordNetLemmatizer
from sklearn.ensemble import AdaBoostClassifier
from nltk import word_tokenize
from nltk.stem.porter import PorterStemmer
import os
from sklearn.base import BaseEstimator, TransformerMixin

#calculate distance import
import geopy.distance

#whastcooking imports#
from whatscooking.whatscooking import*
import csv



def loggedin(view):
    def mod_view(request):
        login_form = UserLogInForm()
        if 'username' in request.session:
            username = request.session['username']
            try: user = UserProfile.objects.get(username=username)
            except UserProfile.DoesNotExist: raise Http404('User does not exist')
            return view(request)
        else:
            return render(request, 'index.html', {'login_form': login_form, 'loggedIn': False})
    return mod_view


def scrape ():

    url_list = [
    'https://www.opentable.com/r/kilikya-mile-end-london?avt=eyJ2IjoxLCJtIjowLCJwIjowfQ&corrId=5f970422-07b4-47e0-823b-bcd5829a7555&p=2&sd=2019-01-20%2019%3A00',
    'https://www.opentable.com/palmers-restaurant?avt=eyJ2IjoxLCJtIjowLCJwIjowfQ&corrId=ea5e8fc7-ed70-4763-88b7-febc3ad1daf5&p=2&sd=2019-01-29+19%3A00',
    'https://www.opentable.com/r/sultan-sofrasi-london?avt=eyJ2IjoxLCJtIjowLCJwIjowfQ&corrId=ea5e8fc7-ed70-4763-88b7-febc3ad1daf5&p=2&sd=2019-01-29+19%3A00',
    'https://www.opentable.com/r/the-widows-son-london?avt=eyJ2IjoxLCJtIjowLCJwIjowfQ&corrId=ea5e8fc7-ed70-4763-88b7-febc3ad1daf5&p=2&sd=2019-01-29+19%3A00',
    'https://www.opentable.com/r/90-degree-melt-london?avt=eyJ2IjoxLCJtIjowLCJwIjowfQ&corrId=ea5e8fc7-ed70-4763-88b7-febc3ad1daf5&p=2&sd=2019-01-29+19%3A00',
    'https://www.opentable.com/verdis-restaurant-london?avt=eyJ2IjoxLCJtIjowLCJwIjowfQ&corrId=ea5e8fc7-ed70-4763-88b7-febc3ad1daf5&p=2&sd=2019-01-29+19%3A00',
    'https://www.opentable.com/r/bacaro-london?avt=eyJ2IjoxLCJtIjowLCJwIjowfQ&corrId=ea5e8fc7-ed70-4763-88b7-febc3ad1daf5&p=2&sd=2019-01-29+19%3A00'
    ]

    for url in url_list:
        source = requests.get(url)
        soup = BeautifulSoup(source.text, 'lxml')


        restaurant_name=soup.find('div', class_="_85098b38").text
        opening=soup.find(itemprop="openingHours").get_text(separator="\n")

        restaurant_desc=soup.find('div', class_="_894dc9d0").text
        description=soup.find(itemprop="description").get_text(separator="\n")

        neighbourhood= soup.find_all("div", class_="_16c8fd5e _1f1541e1")
        d = neighbourhood = soup.find_all("a", class_="f3bf9165")



        address=soup.find(itemprop="streetAddress").get_text()
        geocode_result = gmaps.geocode(address)
        for v in geocode_result:
            lat = v['geometry']['location']['lat']
            lng =  v['geometry']['location']['lng']

        restaurant = Restaurant.objects.create(name=restaurant_name,opening=opening,description=description,long=lng,lat=lat,address=address)
        restaurant.save()

        menu_items = soup.find('div', class_="menu-items__2DRnPKGV")

        for menu_items in soup.find_all('div', class_="menu-item__2ZxJOnTY"):

            try:
                price = menu_items.findChildren()[0].text
                price=price.translate({ord('£'): None})
                price=float(price)
            except:
                price=0.00

            try:
                name = menu_items.findChildren()[1].text
            except:
                name=""

            try:
                desc = menu_items.findChildren()[2].text
            except:
                desc =" "

            if  not name or name.startswith("£"):
                continue
            else:
                menu = Menu_Items.objects.create(item_name=name,item_price=price,item_description=desc,restaurant_name=restaurant)
                menu.save()


    data = Menu_Items.objects.only('item_name','item_description','item_price')

    return data

def runML():

    cook = Coookings().split().train_model().predict().get_metrics()

    return HttpResponse('')

def itemsToJSON():

    data = serializers.serialize('json', Menu_Items.objects.filter(restaurant_name=101), fields=('item_description'))

    file = open('whatscooking/test2.txt','w')
    file.write(data)
    file.close()

    return HttpResponse('')

def updateItemsModel():
    f = open('submission.csv')
    csv_f = csv.reader(f)

    for column in csv_f:
            pk= column[0]
            t = column[1]

            try:
                pk = int(pk)
                item= Menu_Items.objects.get(pk=pk)
                print(item.item_name)
                item.type= str(t)
                item.save()

            except:
                continue

    return HttpResponse('')


def index(request):
    itemsToJSON()
    runML()
    updateItemsModel()


    return render (request,'index.html')

def index2(request):



    return render (request,'index2.html')

def profile(request):


    coords_1 = (51.531441500, -0.037871500)
    coords_2 = (51.4553169, -0.0130913)
    d = geopy.distance.distance(coords_1, coords_2).km

    return render (request,'profile.html')

def addresses (request):
    addresses = Restaurant.objects.order_by('name').values('name','address')
    #print(list(addresses))
    return JsonResponse({'addresses': list(addresses)})


def map(request):
    if request.method == "POST":

        name = request.POST['id']
        type = request.POST['food_type']
        min = request.POST['min']
        max = request.POST['max']



        items= Menu_Items.objects.filter(restaurant_name_id=name).filter(type=type).filter(item_price__range=(min, max)).values('item_name','item_description','item_price')
        print(list(items))
        return JsonResponse({'items': list(items)})


    else:
        restaurants= Restaurant.objects.order_by('name')

        addresses = Restaurant.objects.order_by('name').values('name','address')


        return render (request,'index2.html',{ 'restaurants': restaurants, 'addresses': addresses } )

def plotMap(request):
    if request.method == "GET":

        coordinates = Restaurant.objects.filter().values('name','lat','long','opening','id')
        print(list(coordinates))
    return JsonResponse({'coordinates': list(coordinates)})

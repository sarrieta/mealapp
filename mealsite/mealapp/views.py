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

        print(d)


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

def train():

    data=""
    return data

def index(request):

    return render (request,'index.html')

def profile(request):


    coords_1 = (51.531441500, -0.037871500)
    coords_2 = (51.4553169, -0.0130913)
    d = geopy.distance.distance(coords_1, coords_2).km
    print('distance')
    print(d)

    return render (request,'profile.html')

def addresses (request):
    addresses = Restaurant.objects.order_by('name').values('name','address')
    print(list(addresses))
    return JsonResponse({'addresses': list(addresses)})




def map(request):
    if request.method == "POST":

        name = request.POST['id']
        type = request.POST['food_type']
        min = request.POST['min']
        max = request.POST['max']

        print(name)
        print(type)
        print(min)
        print(max)

        items= Menu_Items.objects.filter(restaurant_name_id=name).filter(type=type).filter(item_price__range=(min, max)).values('item_name','item_description','item_price')
        print(list(items))
        return JsonResponse({'items': list(items)})


    else:
        restaurants= Restaurant.objects.order_by('name')

        addresses = Restaurant.objects.order_by('name').values('name','address')
        print(list(addresses))
        #print(restaurants)
    #    serialiseRestaurants(request)

        return render (request,'map.html',{ 'restaurants': restaurants, 'addresses': addresses } )

def plotMap(request):
    if request.method == "GET":

        coordinates = Restaurant.objects.filter().values('name','lat','long')

    return JsonResponse({'coordinates': list(coordinates)})


def register(request):

     if request.method == "POST":
        registration_form = UserRegForm(request.POST)
        print("in post")

        if registration_form.is_valid():
            print("is valid")
			# normalized data
            username = registration_form.cleaned_data['username']
            username = username.lower()
            password = registration_form.cleaned_data['password']
            re_password = registration_form.cleaned_data['re_password']
            print(username)
            print(password)
            print(re_password)
            # password validation
            if password and re_password:
                if password != re_password:
                    #return error if passwords do not match
                    errorPassword=("The two password fields do not match.")
                    login_form = UserLogInForm()
                    context = {
                        'registration_form': registration_form,
                        'errorPassword':errorPassword
                        }
                    return render(request, 'register.html', context)
                    #sets the user's username and passwords if re_password and password fields match
                else:
                    user = UserProfile(username=username)
                    user.set_password(password)


                    try:
                        user.save()
                    #validation of username uniqueness. Returns an error if user.save fails
                    except IntegrityError:
                        context = {
                            'registration_form': registration_form
                            }

                        return render(request, 'register.html', context)

                    registration_form = UserRegForm()
                    login_form = UserLogInForm()
                    return render(request, 'index.html', {'login_form': login_form, 'registration_form': registration_form, 'loggedIn': False})
            else:
                context = {
                'registration_form': registration_form,
                'errorPassword':'Enter a value in both password fields',
                }

            return render(request, 'register.html', context)

        else:
            print("form isnt valid")
            print(registration_form.errors)
            context = {
            'registration_form': registration_form,
            'loggedIn': False
            }

            return render(request, 'register.html', context)



     else:
         print("NOT in post")
         registration_form = UserRegForm()
         return render(request, 'register.html', {'registration_form': registration_form, 'loggedIn': False})

def login(request):
    if "username" in request.session:
        return redirect('map')
        print('inmap')
    if request.method == "POST":
        login_form = UserLogInForm(request.POST)
        print("in request")
        if 'username' in request.POST and 'password' in request.POST:
            print("credentials found")
            if login_form.is_valid():
                print('login valid')
                # normalized data
                username = login_form.cleaned_data.get("username")
                username = username.lower()
                password = login_form.cleaned_data.get("password")
                #user credentials validation
                user = authenticate(username=username, password=password)

                if user is not None:
                    if user.is_active:
                        request.session['username'] = username
                        request.session['password'] = password
                        print("logged in")
                        """form = UserProfile()
                        member_form = MemberProfile()
                        #populates User Profile form with database values
                        profile = Profile.objects.get(user=user.id)
                        form = UserProfile(initial=model_to_dict(profile))

                        person = Member.objects.get(username=user)
                        #populates Member Profile form with database values
                        member_form = MemberProfile(initial=model_to_dict(person))
                        person = Member.objects.get(id=user.id)"""
                        person = UserProfile.objects.get(username=username)
                        context = {
                            'user': person,
                            'loggedIn': True
                        }
                        print("log in dered")
                        return render(request, 'map.html', context)
                #returns errors if credentials are invalid
                else:
                    print("user is none")
                    context = {

                    'login_form': login_form,
                    }
                    return render(request, 'index.html', context)
            else:
                print("form isnt valid")
                print(login_form.errors)
                context = {

                    'login_form': login_form,
                }
                return render(request, 'login.html', context)

    else:
        print("not in request")
        login_form = UserLogInForm()
        context = {
        'login_form': login_form,
        'loggedIn': False
        }
        return render(request, 'login.html', context)
@loggedin
def logout(request):
	request.session.flush()
	return redirect("/")

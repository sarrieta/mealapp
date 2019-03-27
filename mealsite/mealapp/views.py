from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.http import JsonResponse
import json
from django.core import serializers
#array imports
from django.contrib.postgres.fields import ArrayField
from django_postgres_extensions.models.functions import *
#geocoding imports
import googlemaps
from datetime import datetime
gmaps = googlemaps.Client(key='AIzaSyCpFC94xiuIL1vHEBiGv43sgVga7aJTA1c')
# Scraper imports
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
from .models import *


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
from whatscookingC.whatscookingC import*
import csv



def scrape ():

    delete = Restaurant.objects.all().delete()

    url_list = [
    'https://www.opentable.com/r/kilikya-mile-end-london?avt=eyJ2IjoxLCJtIjowLCJwIjowfQ&corrId=5f970422-07b4-47e0-823b-bcd5829a7555&p=2&sd=2019-01-20%2019%3A00',
    'https://www.opentable.com/palmers-restaurant?avt=eyJ2IjoxLCJtIjowLCJwIjowfQ&corrId=ea5e8fc7-ed70-4763-88b7-febc3ad1daf5&p=2&sd=2019-01-29+19%3A00',
    'https://www.opentable.com/r/sultan-sofrasi-london?avt=eyJ2IjoxLCJtIjowLCJwIjowfQ&corrId=ea5e8fc7-ed70-4763-88b7-febc3ad1daf5&p=2&sd=2019-01-29+19%3A00'
    # 'https://www.opentable.com/r/the-widows-son-london?avt=eyJ2IjoxLCJtIjowLCJwIjowfQ&corrId=ea5e8fc7-ed70-4763-88b7-febc3ad1daf5&p=2&sd=2019-01-29+19%3A00',
    # 'https://www.opentable.com/r/90-degree-melt-london?avt=eyJ2IjoxLCJtIjowLCJwIjowfQ&corrId=ea5e8fc7-ed70-4763-88b7-febc3ad1daf5&p=2&sd=2019-01-29+19%3A00',
    # 'https://www.opentable.com/verdis-restaurant-london?avt=eyJ2IjoxLCJtIjowLCJwIjowfQ&corrId=ea5e8fc7-ed70-4763-88b7-febc3ad1daf5&p=2&sd=2019-01-29+19%3A00',
    # 'https://www.opentable.com/r/bacaro-london?avt=eyJ2IjoxLCJtIjowLCJwIjowfQ&corrId=ea5e8fc7-ed70-4763-88b7-febc3ad1daf5&p=2&sd=2019-01-29+19%3A00',
    # 'https://www.opentable.co.uk/r/rowleys-restaurant-london?avt=eyJ2IjoxLCJtIjoxLCJwIjoxfQ&corrId=4314a95c-763a-43f0-be0c-03931a9b775d&p=2&sd=2019-03-08+19%3A00',
    # 'https://www.opentable.co.uk/r/inamo-soho-london?avt=eyJ2IjoxLCJtIjoxLCJwIjowfQ&corrId=4314a95c-763a-43f0-be0c-03931a9b775d&p=2&sd=2019-03-08+19%3A00',
    # 'https://www.opentable.co.uk/r/blacklock-london-2?avt=eyJ2IjoxLCJtIjoxLCJwIjowfQ&corrId=4314a95c-763a-43f0-be0c-03931a9b775d&p=2&sd=2019-03-08+19%3A00',
    # 'https://www.opentable.co.uk/r/foxlow-soho-london?avt=eyJ2IjoxLCJtIjoxLCJwIjowfQ&corrId=4314a95c-763a-43f0-be0c-03931a9b775d&p=2&sd=2019-03-08+19%3A00',
    # 'https://www.opentable.co.uk/r/maison-du-mezze-london?avt=eyJ2IjoxLCJtIjoxLCJwIjoxfQ&corrId=4314a95c-763a-43f0-be0c-03931a9b775d&p=2&sd=2019-03-08%2019%3A00',
    # 'https://www.opentable.co.uk/r/baluchi-london-2?avt=eyJ2IjoxLCJtIjoxLCJwIjoxfQ&corrId=6c5d52dc-f3d0-4b57-9575-091f6b1f077e&p=2&sd=2019-03-08+19%3A00',
    # 'https://www.opentable.co.uk/r/roast-london?avt=eyJ2IjoxLCJtIjoxLCJwIjoxfQ&corrId=6c5d52dc-f3d0-4b57-9575-091f6b1f077e&p=2&sd=2019-03-08+19%3A00',
    # 'https://www.opentable.co.uk/r/the-ivy-tower-bridge-london?avt=eyJ2IjoxLCJtIjoxLCJwIjowfQ&corrId=6c5d52dc-f3d0-4b57-9575-091f6b1f077e&p=2&sd=2019-03-08+19%3A00',
    # 'https://www.opentable.co.uk/r/kudu-london?avt=eyJ2IjoxLCJtIjoxLCJwIjowfQ&corrId=6c5d52dc-f3d0-4b57-9575-091f6b1f077e&p=2&sd=2019-03-08+19%3A00',
    # 'https://www.opentable.co.uk/gaucho-tower-bridge?avt=eyJ2IjoxLCJtIjoxLCJwIjowfQ&corrId=6c5d52dc-f3d0-4b57-9575-091f6b1f077e&p=2&sd=2019-03-08+19%3A00',
    # 'https://www.opentable.co.uk/r/duddells-london?avt=eyJ2IjoxLCJtIjoxLCJwIjowfQ&corrId=6c5d52dc-f3d0-4b57-9575-091f6b1f077e&p=2&sd=2019-03-08+19%3A00',
    # 'https://www.opentable.co.uk/ting-restaurant-shangri-la-at-the-shard?avt=eyJ2IjoxLCJtIjoxLCJwIjowfQ&corrId=6c5d52dc-f3d0-4b57-9575-091f6b1f077e&p=2&sd=2019-03-08+19%3A00',
    # 'https://www.opentable.co.uk/r/suvlaki-shoreditch-london?avt=eyJ2IjoxLCJtIjoxLCJwIjoxfQ&corrId=8dcbb840-7c90-4fd4-8e52-dbb3f1d118f0&p=2&sd=2019-03-08+19%3A00',
    # 'https://www.opentable.co.uk/r/nobu-shoreditch-london?avt=eyJ2IjoxLCJtIjoxLCJwIjowfQ&corrId=8dcbb840-7c90-4fd4-8e52-dbb3f1d118f0&p=2&sd=2019-03-08+19%3A00',
    # 'https://www.opentable.co.uk/r/morito-hackney-london?avt=eyJ2IjoxLCJtIjoxLCJwIjowfQ&corrId=8dcbb840-7c90-4fd4-8e52-dbb3f1d118f0&p=2&sd=2019-03-08+19%3A00',
    # 'https://www.opentable.co.uk/hoi-polloi?avt=eyJ2IjoxLCJtIjoxLCJwIjowfQ&corrId=8dcbb840-7c90-4fd4-8e52-dbb3f1d118f0&p=2&sd=2019-03-08+19%3A00',
    # 'https://www.opentable.co.uk/r/tapas-brindisa-shoreditch-london?avt=eyJ2IjoxLCJtIjoxLCJwIjoxfQ&corrId=8dcbb840-7c90-4fd4-8e52-dbb3f1d118f0&p=2&sd=2019-03-08+19%3A00',
    # 'https://www.opentable.co.uk/plum-and-spilt-milk?avt=eyJ2IjoxLCJtIjoxLCJwIjoxfQ&corrId=ca2799b1-5e46-4517-9fc4-b6a3658b3767&p=2&sd=2019-03-08+19%3A00',
    # 'https://www.opentable.co.uk/r/st-pancras-brasserie-by-searcys-london?avt=eyJ2IjoxLCJtIjoxLCJwIjowfQ&corrId=ca2799b1-5e46-4517-9fc4-b6a3658b3767&p=2&sd=2019-03-08+19%3A00',
    # 'https://www.opentable.co.uk/r/shaka-zulu-london?avt=eyJ2IjoxLCJtIjoxLCJwIjoxfQ&corrId=ca2799b1-5e46-4517-9fc4-b6a3658b3767&p=2&sd=2019-03-08+19%3A00',
    # 'https://www.opentable.co.uk/r/rossella-london?avt=eyJ2IjoxLCJtIjoxLCJwIjowfQ&corrId=ca2799b1-5e46-4517-9fc4-b6a3658b3767&p=2&sd=2019-03-08+19%3A00',
    # 'https://www.opentable.co.uk/german-gymnasium-restaurant?avt=eyJ2IjoxLCJtIjoxLCJwIjowfQ&corrId=ca2799b1-5e46-4517-9fc4-b6a3658b3767&p=2&sd=2019-03-08+19%3A00'
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
                price=""

            try:
                name = menu_items.findChildren()[1].text
            except:
                name=""

            try:
                desc = menu_items.findChildren()[2].text
            except:
                desc =""

            if  not name or name.startswith("£") or not desc or not price:
                continue
            else:
                x = desc.split()
                # print(x)
                # print('next item')
                # print(' ')


                menu = Menu_Items.objects.create(item_name=name,item_price=price,item_description=desc,restaurant_name=restaurant)

                for i in x:
                    e = menu.ingredients.append(i)
                    i = i.replace(',', '')
                    print(i)
                    Menu_Items.objects.update(ingredients = ArrayAppend('ingredients', i))
                print('next item')
                print(' ')




                menu.save()


    data = Menu_Items.objects.only('item_name','item_description','item_price')

    return data

def itemsToJSON():

    #data = Menu_Items.objects.all().only fields=('ingre'))
    data = serializers.serialize('json', Menu_Items.objects.all(), fields=('item_description','ingredients'))
    #r   = Restaurant.objects.all().values('id')
    #print (list (r))

    file = open('whatscooking/testNotescaped.txt','w')
    file.write(data)
    file.close()

        # Read in the file
    with open('whatscooking/testNotescaped.txt', 'r') as file :
      filedata = file.read()

    # Replace the target string
    filedata = filedata.replace('\\', '')

    # Write the file out again
    with open('whatscooking/test2.txt', 'w') as file:
      file.write(filedata)

    return HttpResponse('')

def runML():

    type = Coookings().split().train_model().predict().get_metrics()
    #cusine = CoookingsC().split().train_model().predict().get_metrics()

    return HttpResponse('')


def updateItemsModel():
    f = open('submission.csv')
    csv_f = csv.reader(f)

    for column in csv_f:
            pk= column[0]
            t = column[1]
            try:
                pk = int(pk)
                item= Menu_Items.objects.filter(pk=pk).update(type=str(t))

            except:
                print('Type cannot be updated')
                print(' ')
                continue

    return HttpResponse('')


def updateItemCuisine():

    f = open('submissionC.csv')
    csv_f = csv.reader(f)

    for column in csv_f:
            pk= column[0]
            t = column[1]

            try:
                pk = int(pk)
                print(pk)
                item= Menu_Items.objects.get(pk=pk)
                print('PK and item matched')
                item.update(type=None)
                print('item updated')
                print(item.cuisine)
                item.save()

            except:
                continue


    return HttpResponse('')

def index(request):
    #scrape()
    itemsToJSON()
    runML()
    # updateItemsModel()
    # #updateItemCuisine()

    return HttpResponse('Index executed')

def index2(request):



    return render (request,'index2.html')

def profile(request):


    coords_1 = (51.531441500, -0.037871500)
    coords_2 = (51.4553169, -0.0130913)
    d = geopy.distance.distance(coords_1, coords_2).km

    return render (request,'profile.html')

def addresses (request):
    addresses = Restaurant.objects.order_by('name').values('name','address')
    ##print(list(addresses))
    return JsonResponse({'addresses': list(addresses)})


def map(request):
    if request.method == "POST":

        name = request.POST['id']
        type = request.POST['food_type']
        cuisine = request.POST['cuisine']
        min = request.POST['min']
        max = request.POST['max']

        if type != 'omnivore':

            items= Menu_Items.objects.order_by('item_price').filter(restaurant_name_id=name).filter(type=type).filter(item_price__range=(min, max)).values('item_name','item_description','item_price')
        else:
            items= Menu_Items.objects.order_by('item_price').filter(restaurant_name_id=name).filter(item_price__range=(min, max)).values('item_name','item_description','item_price')

        #print(list(items))
        return JsonResponse({'items': list(items)})


    else:
        restaurants= Restaurant.objects.order_by('name')

        addresses = Restaurant.objects.order_by('name').values('name','address')
        #print(list(addresses))
        #print('heeey')


        return render (request,'index2.html',{ 'restaurants': restaurants, 'addresses': addresses } )

def plotMap(request):
    if request.method == "POST":

        type = request.POST['food_type']
        cuisine = request.POST['cuisine']
        min = request.POST['min']
        max = request.POST['max']


        restaurants= Restaurant.objects.all().only('id')

        #coordinates = list()

        for r in restaurants:
            #print(r)

            items= Menu_Items.objects.filter(restaurant_name=r).filter(type=type).filter(item_price__range=(min, max)).values('item_name','item_description','item_price')

            if (items):
                #print('yes')
                rest = Restaurant.objects.filter(name=r)
                #print(rest)
                data = serializers.serialize('json', list(rest))
                print()
                #coordinates.append(data)

            else:
                #print('no')
                d=''


        #print(list(coordinates))
        coordinates = Restaurant.objects.filter().values('name','lat','long','opening','id')
        #print(list(coordinates))
    return JsonResponse({'coordinates': list(coordinates)})

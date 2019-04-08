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

#regex
import re



def scrape ():

    delete = Restaurant.objects.all().delete()

    url_list = [
    'https://www.opentable.co.uk/sonmez-salar-sami-t-as-salieri-restaurant?avt=eyJ2IjoxLCJtIjoxLCJwIjoxfQ&corrId=149dbfe2-5b7d-4906-83e0-18e0c3f4a9b9&p=2&sd=2019-04-07+19%3A00',
    'https://www.opentable.co.uk/r/sultan-sofrasi-london?avt=eyJ2IjoxLCJtIjoxLCJwIjowfQ&corrId=51409119-f5c0-4b06-81f7-1a2972e9435b&p=2&sd=2019-04-07%2019%3A00',
    'https://www.opentable.co.uk/r/kilikya-mile-end-london?corrId=51409119-f5c0-4b06-81f7-1a2972e9435b&p=2&sd=2019-04-07+19%3A00',
    'https://www.opentable.co.uk/palmers-restaurant?corrId=51409119-f5c0-4b06-81f7-1a2972e9435b&p=2&sd=2019-04-07+19%3A00',
    'https://www.opentable.co.uk/r/90-degree-melt-london?corrId=51409119-f5c0-4b06-81f7-1a2972e9435b&p=2&sd=2019-04-07+19%3A00',
    'https://www.opentable.co.uk/r/capeesh-restaurant-london?avt=eyJ2IjoxLCJtIjoxLCJwIjowfQ&corrId=a22e62d5-59ad-4bea-898e-4a53820dac1c&p=2&sd=2019-04-07+19%3A00,'
    'https://www.opentable.co.uk/r/drake-and-morgan-t-the-sipping-room-london?avt=eyJ2IjoxLCJtIjoxLCJwIjowfQ&corrId=a22e62d5-59ad-4bea-898e-4a53820dac1c&p=2&sd=2019-04-07+19%3A00',
    'https://www.opentable.co.uk/r/north-pole-bar-and-grill-london?avt=eyJ2IjoxLCJtIjoxLCJwIjoxfQ&corrId=45df4030-612f-4122-95cb-3fcfa82e926c&p=2&sd=2019-04-07+19%3A00',
    'https://www.opentable.co.uk/r/india-garden-london-2?avt=eyJ2IjoxLCJtIjoxLCJwIjowfQ&corrId=a717db31-0f75-451e-8e48-a82000047851&p=2&sd=2019-04-07%2019%3A00',
    'https://www.opentable.co.uk/r/namaaste-kitchen-london?avt=eyJ2IjoxLCJtIjoxLCJwIjoxfQ&corrId=a717db31-0f75-451e-8e48-a82000047851&p=2&sd=2019-04-07+19%3A00',
    'https://www.opentable.co.uk/plum-and-spilt-milk?avt=eyJ2IjoxLCJtIjoxLCJwIjowfQ&corrId=a717db31-0f75-451e-8e48-a82000047851&p=2&sd=2019-04-07+19%3A00',
    'https://www.opentable.co.uk/the-blues-kitchen-camden?avt=eyJ2IjoxLCJtIjoxLCJwIjowfQ&corrId=a717db31-0f75-451e-8e48-a82000047851&p=2&sd=2019-04-07+19%3A00',
    'https://www.opentable.co.uk/r/champor-champor-london',
    'https://www.opentable.co.uk/r/zuaya-london',
    'https://www.opentable.co.uk/r/suito-japanese-london-2?avt=eyJ2IjoxLCJtIjoxLCJwIjoxfQ&corrId=08c27570-4610-4f9f-8eb4-6f4f26b7296d&p=2&sd=2019-04-07+19%3A00',
    'https://www.opentable.co.uk/r/symposium-london?avt=eyJ2IjoxLCJtIjoxLCJwIjowfQ&corrId=51409119-f5c0-4b06-81f7-1a2972e9435b&p=2&sd=2019-04-07+19%3A00',
    'https://www.opentable.co.uk/r/cristinas-barking?avt=eyJ2IjoxLCJtIjoxLCJwIjowfQ&corrId=ab336dd6-6e21-45fe-b50b-244a799f88d4&p=2&sd=2019-04-07+19%3A00',
    'https://www.opentable.co.uk/r/frankie-and-bennys-newham-barking?corrId=ab336dd6-6e21-45fe-b50b-244a799f88d4&p=2&sd=2019-04-07%2019%3A00'

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
                descL=[]
                list_n = []

                filterlist = ['and','the','with','the','and','fried','or','&','sw','grilled','adana','shish','dressing','mixed','leaves',
                'roll','pastry','spicy','hot','of','grated','dill','stuffed','please','ask','vine','green','red','sauce','paste','chopped',
                'baked','a','diced','topped','stuffed','specially','prepared','bed','Sautéed','Sautée','Bottomless','sunday','lunch',
                'baked','a',')','(','roast','F.O.T.D ','cut','de','of','Selection','Selection','ragu','lunch',
                'Superb','elegant','superb','redefined','sparkling','fruity','flowers','touch','yellow','served','ring','cooked','white',
                'char','spit','mixture','Marinated','chops','chargrilled','Knuckle','slow','yellow','served','pieces','Oven','mediterranean',
                'herbs','minced','thin','very','juice','flavoured','thinly','award','winning','country','artisanal','Oven','Seasonal',
                'balsamic','Buckhurst','style','traditional','Roast','sweet','light','Spanish','omelette','deep','delicious','each','classic',
                'tights','sprinkled','seeds','dip','two','soft','both','buns','8oz','4oz','toasted','favourite','crushed',
                'smoked','Shredded','Nourishing','brown','breast','baby','cubed','layer','layered','tangy','ripe','salad','Stone-baked',
                'always','smashed','black','ree-range','pasta','stew','compote','semifreddo','pipping',
                'american','wedges','Chipotle','but','without','Smothered','in','cooling','All-American',
                '-','wedges','no-ham','blt','without','Smothered','in','cooling','AllAmerican',
                'corn-battered','battered','bun','extra','toppings','Veggies','(Burger,Lettuce,Tomato)','fun-fair','staple',
                'Flavors','North','corndog','cornbattered','on','vegan','africa','flavorful','wine','Riesling',
                'Brooklyn','pairing','house','roasted','FOTD','Blanc','Sauvignon','Sunblush','rocketwine','blanc','desperados',
                'shredded','fun','take','cook','oreo','8','4','to','to,','steamed','excellent','simply','many','our','dishes','three','encased',
                'pop','out','whet','appetite','version','bowl','sip','though','presented,','phones','Camera','pool','tranquil','our','dishes','melted']

                for l in x:
                        l = re.sub('[^A-Za-z0-9]+', '', l)
                        l = l.replace(',', '')
                        list_n.append(l)

                for word in list_n:
                   if word.lower() not in filterlist:
                        descL.append(word)

                str1 = list(descL)
                ###

                out=[]
                data = {}

                data['fields'] = []
                for w in descL:

                    data['fields'].append(w)

                out.append(data)

                with open('whatscooking/menuItem.txt', 'w') as outfile:
                    json.dump(out, outfile)

                with open('whatscookingC/menuItem.txt', 'w') as outfile:
                    json.dump(out, outfile)

                ####
                cuisine = Coookings().split().train_model().predict().get_metrics()
                type = CoookingsC().split().train_model().predict().get_metrics()

                #####
                f = open('submission.csv')
                csv_f = csv.reader(f)

                for column in csv_f:
                        pk= column[0]
                        c = column[1]
                        try:
                            if (c!='cuisine'):
                                print('cuisine is:')
                                print(c)

                            # pk = int(pk)
                            # item= Menu_Items.objects.filter(pk=pk).update(type=str(t))
                            else:
                                continue
                        except:
                            print('Cuisine cannot be updated')
                            print(' ')
                            continue

                #####
                f = open('submissionC.csv')
                csv_f = csv.reader(f)

                for column in csv_f:
                        pk= column[0]
                        t = column[1]
                        try:
                            if (t!='cuisine'):
                                print('type is:')
                                print(t)
                            else:
                                continue
                        except:
                            print('Type cannot be updated')
                            print(' ')
                            continue


                ####

                filtered = str(name.lower())
                some_list = ['chicken', 'lamb', 'beef', 'kebab','prawn','prawns','wings','wing','steak','prawn','cod','sushi','calamari','pork','salmon','rib','ribs',
                'duck', 'turkey','sausage','sausages']

                if any(filtered in s for s in some_list):
                    print('word found')
                    print(name)
                    t ='omnivore'
                    menu = Menu_Items.objects.create(item_name=name,item_price=price,item_description=desc,restaurant_name=restaurant,cuisine=c,type=t)

                    for i in str1:
                        e = menu.ingredients.append(i)
                        i = i.replace(',', '')
                        #print(i)
                        Menu_Items.objects.update(ingredients = ArrayReplace('ingredients', i, i))


                    menu.save()
                else:
                    menu = Menu_Items.objects.create(item_name=name,item_price=price,item_description=desc,restaurant_name=restaurant,cuisine=c,type=t)

                    for i in str1:
                        e = menu.ingredients.append(i)
                        i = i.replace(',', '')
                        #print(i)
                        Menu_Items.objects.update(ingredients = ArrayReplace('ingredients', i, i))


                    menu.save()






    data = ''

    return data


def index(request):
    scrape()

    return HttpResponse('Index executed')

def index2(request):

    return render (request,'index2.html')


def addresses (request):
    addresses = Restaurant.objects.order_by('name').values('name','address')

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


        return render (request,'index2.html',{ 'restaurants': restaurants, 'addresses': addresses } )

def plotMap(request):
    if request.method == "POST":

        type = request.POST['food_type']
        cuisine = request.POST['cuisine']
        min = request.POST['min']
        max = request.POST['max']


        restaurants= Restaurant.objects.all().only('id')


        for r in restaurants:
            #print(r)

            items= Menu_Items.objects.filter(restaurant_name=r).filter(type=type).filter(item_price__range=(min, max)).values('item_name','item_description','item_price')

            if (items):
                rest = Restaurant.objects.filter(name=r)
                data = serializers.serialize('json', list(rest))
                print()

            else:

                d=''


        coordinates = Restaurant.objects.filter().values('name','lat','long','opening','id')
        #print(list(coordinates))
    return JsonResponse({'coordinates': list(coordinates)})

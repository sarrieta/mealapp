from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from multiselectfield import MultiSelectField

from django_google_maps import fields as map_fields

class Rental(models.Model):
    address = map_fields.AddressField(max_length=200)
    geolocation = map_fields.GeoLocationField(max_length=100)

class Menu_Items(models.Model):
    type = models.CharField(blank=True,max_length=30)
    item_name = models.CharField(blank=False, default=None,max_length=30)
    item_description = models.CharField(blank=False, default=None,max_length=500)
    item_price = models.FloatField(max_length=2,blank=False, default=None)
    restaurant_name= models.CharField(blank=False,max_length=15)
    class Meta:
        verbose_name = "Menu Item"
        verbose_name_plural = "Menu Items"
    def __str__(self):
        return self.item_name


class Restaurant(models.Model):
    name= models.CharField(blank=False, default=None,max_length=30)
    opening= models.CharField(blank=False, default=None,max_length=30)
    menu_items = models.ManyToManyField(
        blank=True,
        to=Menu_Items,
        symmetrical=False,
        related_name='related_to'
    )
    class Meta:
        verbose_name = "Restaurant"
        verbose_name_plural = "Restaurants"
    def __str__(self):
        return self.name

class Preferences(models.Model):
    #choices = (('vegan', 'Vegan'),
                         #('halal', 'Halal'))
    #preferences = MultiSelectField(choices=choices)
    preferences= models.CharField(blank=False, default=None,max_length=15)
    class Meta:
        verbose_name_plural = "preferences"
    def __str__(self):
        return self.preferences


class UserProfile(User):
    preferences = models.ManyToManyField(
        blank=True,
        to=Preferences,
        symmetrical=False,
        related_name='related_to'
    )
    def __str__(self):
        return self.username
"""class Menu(models.Model):
    name = models.CharField(blank=False, default="test",max_length=30)
    menu_items = models.ManyToManyField(
        blank=True,
        to=Menu_Items,
        symmetrical=False,
        related_name='related_to'
    )
    class Meta:
        verbose_name = "Menu Item"
        verbose_name_plural = "Menu Items"
    def __str__(self):
        return self.item_name"""

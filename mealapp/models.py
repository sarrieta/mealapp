from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

class Restaurant(models.Model):
    name= models.CharField(blank=False, default=None,max_length=100)
    opening= models.TextField(null=True, default=None)
    long = models.DecimalField(null=True,max_digits=15, decimal_places=9)
    lat = models.DecimalField(null=True,max_digits=15, decimal_places=9)
    description= models.TextField(null=True, default=None)
    address= models.CharField(null=True,blank=True, default=None,max_length=100)


    class Meta:
        verbose_name = "Restaurant"
        verbose_name_plural = "Restaurants"
    def __str__(self):
        return self.name

class Menu_Items(models.Model):
    type = models.CharField(blank=True,max_length=30)
    cuisine = models.CharField(blank=True,max_length=30)
    item_name = models.CharField(blank=False, default=None,max_length=100)
    item_description = models.TextField(null=True, default=None)
    item_price = models.FloatField(max_length=2,blank=False, default=None)
    ingredients = ArrayField(models.CharField(max_length = 1000), default = list)
    restaurant_name= models.ForeignKey(
    Restaurant,
        on_delete=models.CASCADE,
    )
    class Meta:
        verbose_name = "Menu Item"
        verbose_name_plural = "Menu Items"
    def __str__(self):
        return self.item_name

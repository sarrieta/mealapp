from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from multiselectfield import MultiSelectField

class Restaurant(models.Model):
    name= models.CharField(blank=False, default=None,max_length=30)
    opening= models.TextField(null=True, default=None)
    long = models.DecimalField(null=True,max_digits=15, decimal_places=9)
    lat = models.DecimalField(null=True,max_digits=15, decimal_places=9)
    description= models.TextField(null=True, default=None)
    address= models.CharField(null=True,blank=True, default=None,max_length=60)

    class Meta:
        verbose_name = "Restaurant"
        verbose_name_plural = "Restaurants"
    def __str__(self):
        return self.name

class Menu_Items(models.Model):
    type = models.CharField(blank=True,max_length=30)
    item_name = models.CharField(blank=False, default=None,max_length=30)
    item_description = models.CharField(blank=False, default=None,max_length=500)
    item_price = models.FloatField(max_length=2,blank=False, default=None)
    restaurant_name= models.ForeignKey(
    Restaurant,
        on_delete=models.CASCADE,
    )
    class Meta:
        verbose_name = "Menu Item"
        verbose_name_plural = "Menu Items"
    def __str__(self):
        return self.item_name




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

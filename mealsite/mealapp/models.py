from django.db import models




class Menu(models.Model):
    type = models.CharField(blank=True,max_length=15)
    item_name = models.CharField(blank=False, default=None,max_length=15)
    item_description = models.CharField(blank=False, default=None,max_length=500)
    item_price = models.FloatField(max_length=2,blank=False, default=None)
    restaurant_name= models.CharField(blank=False,max_length=15)
    class Meta:
        verbose_name = "Menu"
        verbose_name_plural = "Menus"

class Restaurant(models.Model):
    name= models.CharField(blank=False, default=None,max_length=15)
    long = models.DecimalField(max_digits=9, decimal_places=6)
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    class Meta:
        verbose_name = "Restaurant"
        verbose_name_plural = "Restaurants"

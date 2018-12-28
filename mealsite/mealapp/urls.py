

from django.urls import path, include
from mealapp import views
from django.conf.urls import url


urlpatterns = [
	path('',views.index, name='index'),
	path('search/',views.search, name='search'),
]

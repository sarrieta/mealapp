

from django.urls import path, include
from mealapp import views
from django.conf.urls import url


urlpatterns = [
	path('',views.index, name='index'),
	path('index2',views.index2, name='index2'),
	path('map/',views.map, name='map'),
	path('register/',views.register, name='register'),
	path('login/',views.login, name='login'),
	path('logout/',views.logout, name='logout'),
	path('profile/',views.profile, name='profile'),
	path('plotMap/',views.plotMap, name='plotMap'),
	path('addresses/',views.addresses, name='addresses'),

]

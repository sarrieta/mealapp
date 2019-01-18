

from django.urls import path, include
from mealapp import views
from django.conf.urls import url


urlpatterns = [
	path('',views.index, name='index'),
	path('map/',views.map, name='map'),
	path('register/',views.register, name='register'),
	path('login/',views.login, name='login'),
	path('logout/',views.logout, name='logout'),

]

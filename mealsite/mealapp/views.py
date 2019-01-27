from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.http import JsonResponse
####

# Scraper imports
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
from .models import *
from .forms import *

User = get_user_model()



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



def index(request):

	return render (request,'index.html')

def map(request):
    if request.method == "POST":
        name = request.POST['restaurant_name_oncard']
        items= Menu_Items.objects.filter(restaurant_name=name).values('item_name','item_description','item_price')

        return JsonResponse({'items': list(items)})

    else:
        restaurants= Restaurant.objects.order_by('name')
        #print(restaurants)

        return render (request,'map.html',{ 'restaurants': restaurants } )







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

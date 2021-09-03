from main_app.models import Spell
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from os import name
from django.http import response
import requests
import json

# Create your views here.
#home view
class Home(LoginView):
  template_name = 'home.html'
#about view
def about(request):
  return render(request, 'about.html')
#character index view
@login_required
def char_index(request):
  return HttpResponse('<h1>this is char index page</h1>')

def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in
      login(request, user)
      return redirect('characters_index')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'signup.html', context)

def characters_index(request):
  return render(request, '')

def convert(obj):
  text = json.dumps(obj, sort_keys=True, indent=2)

# create and update function makes these calls
def spell_api_call(request):
  char_class = 'bard'
  level = '1'
  response = requests.get(f"https://www.dnd5eapi.co/api/classes/{char_class}/levels/{level}/spells").json()["results"]

  for res in response:
    spell,_ = Spell.objects.get_or_create(name=res["name"])
    # add to character
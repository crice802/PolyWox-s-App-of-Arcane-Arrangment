from .models import Character, Spell, Photo
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from os import name
from django.http import response
import requests
import json
import uuid
import boto3

S3_BASE_URL = 'https://s3.us-east-1.amazonaws.com/'
BUCKET = 'arcanearrangement'
# Create your views here.
#home view
class Home(LoginView):
  template_name = 'home.html'
#about view
def about(request):
  return render(request, 'about.html')
#character index view
@login_required
def character_index(request):
  characters = Character.objects.filter(player=request.user)
  return render(request, 'characters/index.html', {
    'characters': characters
  })
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

@login_required
def characters_index(request):
  characters = Character.objects.filter(player=request.user)
  return render(request, 'characters/index.html', { 'characters': characters })

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

def characters_detail(request, character_id):
  character = Character.objects.get(id=character_id)
  return render(request, 'characters/detail.html', { 
    'character': character
  })

class CharacterCreate(LoginRequiredMixin ,CreateView):
  model = Character
  fields = ['name', 'char_class', 'level', 'player']

  def form_valid(self, form):
    form.instance.player = self.request.user

    return super().form_valid(form)

class CharacterUpdate(LoginRequiredMixin ,UpdateView):
  model = Character
  fields = ['level']

class CharacterDelete(LoginRequiredMixin ,DeleteView):
  model = Character
  success_url = '/characters/'

def add_photo(request, character_id):
  # photo-file will be the "name" attribute on the <input type="file">
  photo_file = request.FILES.get('photo-file', None)
  if photo_file:
    s3 = boto3.client('s3')
    # need a unique "key" for S3 / needs image file extension too
		# uuid.uuid4().hex generates a random hexadecimal Universally Unique Identifier
    # Add on the file extension using photo_file.name[photo_file.name.rfind('.'):]
    key = uuid.uuid4().hex + photo_file.name[photo_file.name.rfind('.'):]
    # just in case something goes wrong
    try:
      s3.upload_fileobj(photo_file, BUCKET, key)
      # build the full url string
      url = f"{S3_BASE_URL}{BUCKET}/{key}"
      # we can assign to character_id or character (if you have a character object)
      photo = Photo(url=url, character_id=character_id)
      # Remove old photo if it exists
      character_photo = Photo.objects.filter(character_id=character_id)
      if character_photo.first():
        character_photo.first().delete()
      photo.save()
    except Exception as err:
      print('An error occurred uploading file to S3: %s' % err)
  return redirect('characters_detail', character_id=character_id)


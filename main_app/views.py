from django.conf.urls import url
from django.db.models import fields
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
from .forms import SpellForm
from main_app import models

# CHAR_LEVEL =f"{Character.level}"
# CHAR_CLASS =f"{Character.char_class}"
SPELL_URL =f"{Spell.url}"
API_BASE_URL = 'https://www.dnd5eapi.co'
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
  return render(request, 'characters/index.html', { 'characters': characters})

# create  function makes this call
@login_required
def spell_level_search(request, character_id):
  character = Character.objects.get(id=character_id)
  response = requests.get(f"{API_BASE_URL}/api/classes/{character.char_class}/levels/{character.level}/spells")
  spelldata = response.json()
  for res in spelldata['results']:
    spell = Spell.objects.get_or_create(name=res["name"], url=res["url"])[0]
    spell_id = spell.id
    Character.objects.get(id=character_id).spell_list.add(spell_id)

  return render(request, 'characters/detail.html',
   {
    'character': character
  })

# class SpellCreate(CreateView):
#   model = Spell
#   fields = '__all__'
@login_required
def spell_details(request, spell_id):
 
  spell = Spell.objects.get(id=spell_id)
  response = requests.get(f"{API_BASE_URL}{spell.url}")
  spelldata = response.json()
  print(spelldata)
  return render(request, 'main_app/spell_detail.html', {
    "name": spelldata['name'], "level": spelldata['level'], 'desc': spelldata['desc'], 'range': spelldata['range'], 'duration': spelldata['duration'], 'casting_time': spelldata['casting_time'], 
  })
 

@login_required
def characters_detail(request, character_id):
  character = Character.objects.get(id=character_id)
  spells_character_does_not_have = Spell.objects.exclude(id__in = character.spell_list.all().values_list('id'))
  return render(request, 'characters/detail.html', { 
    'character': character, 'spells': spells_character_does_not_have
  })

class CharacterCreate(LoginRequiredMixin ,CreateView):
  model = Character
  fields = ['name', 'char_class', 'level', 'player']

  def form_valid(self, form):
    form.instance.player = self.request.user

    return super().form_valid(form)

# def character_update(request, character_id, spell_id):
#   character = Character.objects.get(id=character_id)
#   new_spell = None
#   form = SpellForm(request.POST)
#   if form.is_valid():
#     new_spell = form.save(commit=False)
#     new_spell.spell_id = spell_id
#     new_spell.save()
#   else:
#     form = SpellForm()
#   return redirect('characters_detail', character_id=character_id)
class CharacterUpdate(LoginRequiredMixin ,UpdateView):
  model = Character
  fields = ['level', 'spell_list']

class CharacterDelete(LoginRequiredMixin ,DeleteView):
  model = Character
  success_url = '/characters/'

@login_required
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

@login_required
def assoc_spell(request, character_id, spell_id):
  Character.objects.get(id=character_id).spell_list.add(spell_id)
  return redirect('characters_detail', character_id=character_id)

class SpellList(LoginRequiredMixin ,ListView):
  model = Spell
  fields = ['name']

class SpellDetail(LoginRequiredMixin ,DetailView):
  model = Spell


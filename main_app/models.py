from django.db import models
from django.db.models.fields import CharField
from django.urls import reverse
from django.contrib.auth.models import User
import requests
# Create your models here.
CLASS_CHOICE = (
  ('barbarian', 'barbarian'),
  ('bard', 'bard'),
  ('cleric', 'cleric'),
  ('druid', 'druid'),
  ('fighter', 'fighter'),
  ('monk', 'monk'),
  ('paladin', 'paladin'),
  ('ranger', 'ranger'),
  ('rogue', 'rogue'),
  ('sorcerer', 'sorcerer'),
  ('warlock', 'warlock'),
  ('wizard', 'wizard')
)

class Character(models.Model):
  player = models.ForeignKey(User, on_delete=models.CASCADE)
  name = models.CharField(max_length=50)
  char_class = models.CharField(max_length=8,
  choices=CLASS_CHOICE,
  default=CLASS_CHOICE[0][0]
  )
  level = models.IntegerField(max=20, min=1)
  spell_list = models.CharField()
  

class Photo(models.Model):
  url = models.CharField(max_length=250)
  character = models.OneToOneField(Character, on_delete=models.CASCADE)
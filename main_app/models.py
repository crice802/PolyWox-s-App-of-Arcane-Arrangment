
from django.db import models
from django.db.models.fields import CharField
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

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
class Spell(models.Model):
  name = models.CharField(max_length=250)
  url = models.CharField(max_length=250)
  

  def __str__(self):
    return self.name
  
  def get_absolute_url(self):
      return reverse("spells_detail", kwargs={"spell_id": self.id})
  

class Character(models.Model):
  player = models.ForeignKey(User, on_delete=models.CASCADE)
  name = models.CharField(max_length=50)
  char_class = models.CharField(max_length=9,
  choices=CLASS_CHOICE,
  default=CLASS_CHOICE[0][0]
  )
  level = models.IntegerField(
    default=1,
    validators=[MaxValueValidator(20), MinValueValidator(1)]
  )
  spell_list = models.ForeignKey(Spell, blank=True, null=True, on_delete=models.CASCADE)
  

  def __str__(self):
    return self.name

  def get_absolute_url(self):
      return reverse("characters_detail", kwargs={"character_id": self.id})
  
  

class Photo(models.Model):
  url = models.CharField(max_length=250)
  character = models.OneToOneField(Character, on_delete=models.CASCADE)

  def __str__(self):
    return f"Photo for character_id: {self.character_id} @{self.url}"


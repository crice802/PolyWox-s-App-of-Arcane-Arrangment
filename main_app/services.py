from os import name
from django.http import response
import requests
import json
from models import Character

def convert(obj):
  text = json.dumps(obj, sort_keys=True, indent=2)

response = requests.get("https://www.dnd5eapi.co/api/classes/{char_class}/levels/{level}/spells")

spell_list = []

for res in response.json():
  spell_list.append({ "name": res["name"], "index": res["index"], "url": res["url"] })

  convert(spell_list)
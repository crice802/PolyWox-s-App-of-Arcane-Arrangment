from django.forms import ModelForm
from .models import Spell

class SpellForm(ModelForm):
  class Meta:
    model = Spell
    fields = ['name', 'url']
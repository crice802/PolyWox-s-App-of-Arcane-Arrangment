from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
#home view
def home(request):
  return HttpResponse('<h1>Sanity Check</h1>')
#character index view
def char_index(request):
  return HttpResponse('<h1>this is char index page</h1>')
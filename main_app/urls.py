from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('characters-index/', views.char_index, name='character_index')
]

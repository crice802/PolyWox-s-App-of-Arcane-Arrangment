from os import name
from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),

    path('about/', views.about, name='about'),

    path('characters/', views.character_index, name='character_index'),

    path('accounts/signup/', views.signup, name='signup'),

    path('characters/<int:character_id>/', views.characters_detail, name='characters_detail')

]

from os import name
from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),

    path('about/', views.about, name='about'),

    path('characters/', views.characters_index, name='characters_index'),

    path('accounts/signup/', views.signup, name='signup'),

    path('characters/<int:character_id>/', views.characters_detail, name='characters_detail'),

    path('characters/create/', views.CharacterCreate.as_view(), name='characters_create'),

    path('characters/<int:pk>/update/', views.CharacterUpdate.as_view(), name='characters_update'),

    path('characters/<int:pk>/delete/', views.CharacterDelete.as_view(), name='characters_delete'),

    path('characters/<int:character_id>/add_photo/', views.add_photo, name='add_photo'),

]

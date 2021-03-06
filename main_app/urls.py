from os import name
from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),

    path('characters/', views.characters_index, name='characters_index'),

    path('accounts/signup/', views.signup, name='signup'),

    path('characters/<int:character_id>/', views.characters_detail, name='characters_detail'),

    path('characters/create/', views.CharacterCreate.as_view(), name='characters_create'),

    path('characters/<int:pk>/update/', views.CharacterUpdate.as_view(), name='characters_update'),

    path('characters/<int:pk>/delete/', views.CharacterDelete.as_view(), name='characters_delete'),

    path('characters/<int:character_id>/add_photo/', views.add_photo, name='add_photo'),

    path('characters/<int:character_id>/assoc_spell/<int:spell_id>/', views.assoc_spell, name='assoc_spell'),

    path('characters/<int:character_id>/spells/create/', views.spell_level_search, name='spells_create'),
    
    path('spells/create/', views.spell_level_search, name='spells_create'),

    path('spells/<int:spell_id>/', views.spell_details, name='spells_detail'),

    path('spells/', views.SpellList.as_view(), name='spells_index'),

]

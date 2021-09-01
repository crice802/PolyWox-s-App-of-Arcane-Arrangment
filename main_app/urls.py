from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),

    path('characters/', views.char_index, name='character_index'),

    path('accounts/signup/', views.signup, name='signup'),

]

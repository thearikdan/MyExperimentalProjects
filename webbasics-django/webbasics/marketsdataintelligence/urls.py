from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name ='mdi-home'),
    path('about/', views.about, name ='mdi-about'),
]

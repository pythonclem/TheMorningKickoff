from django.urls import path
from . import views

urlpatterns = [
    path('teams/', views.getTeams),
    path('team/<str:pk>/', views.getTeam),
    path('createuser/', views.createUser) 
]
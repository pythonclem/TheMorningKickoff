from django.urls import path
from . import views
from . import views1

urlpatterns = [
    path('teams/', views.getTeams),
    path('team/<str:pk>/', views.getTeam),
    path('createuser/', views1.CreateUserView.as_view()) 
]
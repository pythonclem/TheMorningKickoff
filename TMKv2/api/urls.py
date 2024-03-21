from django.urls import path
from . import views
from . import views1

urlpatterns = [
    path('teams/', views.getTeams),
    path('team/<str:pk>/', views.getTeam),
    path('users/', views1.UserView.as_view(), name='users'),
    path('users/<int:pk>/', views1.UserView.as_view(), name='user_detail'),]
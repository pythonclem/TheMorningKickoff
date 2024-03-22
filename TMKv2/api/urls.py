from django.urls import path
from . import views
from . import views

urlpatterns = [
    path('teams/', views.TeamView.as_view(), name = 'teams'),
    path('teams/<int:pk>/', views.TeamView.as_view(), name = 'team_detail'),
    path('users/', views.UserView.as_view(), name='users'),
    path('users/<int:pk>/', views.UserView.as_view(), name='user_detail'),]
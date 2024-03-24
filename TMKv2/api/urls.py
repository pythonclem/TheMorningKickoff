from django.urls import path
from . import views
from . import views

urlpatterns = [
    path('teams/', views.TeamView.as_view(), name = 'teams'),
    path('teams/<int:pk>/', views.TeamView.as_view(), name = 'team_detail'),
    path('users/', views.UserView.as_view(), name='users'),
    path('users/<int:pk>/', views.UserView.as_view(), name='user_detail'),
    path('leagues/', views.LeagueView.as_view(), name = 'teams'),
    path('leagues/<int:pk>/', views.LeagueView.as_view(), name = 'team_detail'),
    path('updatescores/', views.ScoreUpdaterView.as_view(), name = 'scoreupdater'),
    path('updatedatetime/', views.DateTimeUpdaterView.as_view(), name = 'dateupdater'),
    path('findnewmatches/', views.MatchAdderView.as_view(), name = 'matchupdater'),
    
    ]
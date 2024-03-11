from django.urls import path
from . import views
urlpatterns = [
    path('leagues/', views.leagues, name="leagues"),
    path('league/<str:pk>/', views.league, name="league"),
    path('team/<str:pk>/', views.team, name="team"),
]
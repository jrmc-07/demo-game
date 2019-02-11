from django.urls import path

from . import views

urlpatterns = [
    path('api-players', views.PlayerList.as_view()),
    path('api-player/<int:player_id>', views.PlayerDetails.as_view()),
]

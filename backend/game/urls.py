from django.urls import path
from rest_framework import routers

from . import views


router = routers.SimpleRouter()
router.register(r'games', views.GameViewSet)
router.register(r'players', views.PlayerViewSet)
urlpatterns = router.urls

# urlpatterns = [
#     path('players', views.PlayerList.as_view()),
#     path('players/<int:player_id>', views.PlayerDetails.as_view()),
# ]

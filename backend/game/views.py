import json
from django.core.serializers import serialize
from django.shortcuts import HttpResponse, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db import transaction
from django.views.generic import View
from rest_framework import mixins, viewsets
from rest_framework.response import Response

from .forms import PlayerForm
from .mixins import MultiSerializerViewSetMixin
from .models import Game, Player
from .serializers import (
    GameSerializer,
    PlayerSerializer,
    PlayerCreateSerializer,
    PlayerListSerializer,
    PlayerUpdateSerializer,
)


class GameViewSet(mixins.CreateModelMixin,
                  viewsets.GenericViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer


class PlayerViewSet(MultiSerializerViewSetMixin,
                    mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    """
    ViewSet for players playing on the *latest* game.
    """
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    serializer_action_classes = {
        'create': PlayerCreateSerializer,
        'list': PlayerListSerializer,
        'update': PlayerUpdateSerializer,
    }

    def get_queryset(self):
        """
        We filter the Players by the latest game here.
        """
        return Player.objects.filter(game=Game.objects.last())

    def perform_create(self, serializer):
        with transaction.atomic():
            latest_game = Game.objects.last()
            # get position based on last person in the game
            try:
                last_position = (Player.objects
                                 .filter(game=latest_game)
                                 .order_by('position')
                                 .last().position) + 1
            except AttributeError:
                # no players yet
                last_position = latest_game.position_counter
            serializer.save(position=last_position, game=latest_game)

    def update(self, request, pk=None):
        # print(request.data)
        # request.data.pop('action', None)
        # print(request.data)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


@method_decorator(csrf_exempt, name='dispatch')
class PlayerList(View):
    def get(self, request):
        players = Player.objects.all()
        return HttpResponse(serialize("json", players),
                            content_type="application/json")


    def post(self, request):
        form = PlayerForm(json.loads(request.body.decode('utf-8')))
        if form.is_valid():
            form.save()
            return HttpResponse(status=201)
        return HttpResponse(status=400)


@method_decorator(csrf_exempt, name='dispatch')
class PlayerDetails(View):
    def get(self, request, player_id):
        player = get_object_or_404(Player, pk=player_id)
        return HttpResponse(serialize("json", [player,]),
                            content_type="application/json")


    def put(self, request, player_id):
        player = get_object_or_404(Player, pk=player_id)
        form = PlayerForm(json.loads(request.body.decode('utf-8')),
                          instance=player)
        if form.is_valid():
            form.save()
            return HttpResponse(status=200)
        return HttpResponse(status=400)


    def delete(self, request, player_id):
        player = get_object_or_404(Player, pk=player_id)
        player.delete()
        return HttpResponse(status=200)

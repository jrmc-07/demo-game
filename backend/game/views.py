from django.core.serializers import serialize
from django.shortcuts import HttpResponse, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.generic import View

from .models import Player

class PlayerList(View):
    def get(self, request):
        players = Player.objects.all()
        return HttpResponse(serialize("json", players),
                            content_type="application/json")


    @csrf_exempt
    def post(self, request):
        pass


    @csrf_exempt
    def put(self, request):
        pass

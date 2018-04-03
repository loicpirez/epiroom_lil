from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from datetime import datetime
from Api.models import Room
from .models import GlobalVar
import json

import os

from django.db import transaction

@transaction.atomic
def index(req):
    now = datetime.now()
    path = os.getcwd()
    nb_room = []
    for room in Room.objects.filter():
        for svg_id in room.svg_ids.split(';'):
            if svg_id not in nb_room and Room.objects.filter(name__icontains=svg_id, show=True):
                nb_room.append(svg_id)
    nb_room = len(nb_room)
    max_col = int(nb_room / 2)
    try:
        svg_path = GlobalVar.objects.get(name="SVG_path")
    except:
        return HttpResponse("Please Try Later")
    with open(svg_path.value) as svg_file:
        next(svg_file)
        svg = svg_file.read()
    return render(req, 'index.html', locals())

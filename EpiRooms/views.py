from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from datetime import datetime
from Api.models import Room
from .models import GlobalVar
import json
from EpiRooms.settings import BASE_DIR
import uuid 

import os

from django.db import transaction

@transaction.atomic
def index(req):
    refresh = int(GlobalVar.objects.get(name="auto_refresh").value)
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
        svg_path = os.path.join(BASE_DIR, GlobalVar.objects.get(name="SVG_path").value)
    except:
        return HttpResponse("Please Try Later")
    with open(svg_path) as svg_file:
        next(svg_file)
        svg = svg_file.read()
    return render(req, 'index.html', locals())


def cmd(req):
    c = GlobalVar.objects.filter(name__startswith="cmd_", name__contains="").first()
    value = c.value if c else ""
    if c:
        c.value = ""
        c.save()
    return JsonResponse({
        "id": "", #req.META['HTTP_X_REAL_IP'],
        "test": uuid.uuid1(),
        "cmd": value
    }, safe=False)

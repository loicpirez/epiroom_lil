from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from datetime import datetime
from Api.models import Room
from .models import GlobalVar
import json

import os

def index(req):
    now = datetime.now()
    path = os.getcwd()
    nb_room = Room.objects.filter(show=True).count()
    #try:
    svg_path = GlobalVar.objects.get(name="SVG_path")
    #except:
    #    return HttpResponse("Please Try Later")
    with open(svg_path.value) as svg_file:
        next(svg_file)
        svg = svg_file.read()
    return render(req, 'index.html', locals())

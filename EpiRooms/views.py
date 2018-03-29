from django.shortcuts import render, redirect
from django.http import JsonResponse
from datetime import datetime
from Api.models import Room
import json

import os

def index(req):
    now = datetime.now()
    path = os.getcwd()
    nb_room = Room.objects.filter(show=True).count()
    with open('templates/Epitech.svg') as svg_file:
        next(svg_file)
        svg = svg_file.read()
    return render(req, 'index.html', locals())

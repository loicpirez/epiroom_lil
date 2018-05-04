from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from datetime import timedelta, datetime
from django.views.decorators.csrf import csrf_exempt
from subprocess import run, PIPE
import requests, json, os

from EpiRooms.models import GlobalVar
from Api.models import Room, Booking

def get_bookablerooms():
    now = timezone.now()
    rooms = []
    for room in Room.objects.filter(bookable=True):
        booking = Booking.objects.filter(room=room, start__lt=now, end__gt=now)
        state = "success" if not booking else "danger"
        state = "muted" if not room.show else state
        rooms.append({'id': room.id, 'name': room.name, 'svg_ids': room.svg_ids, 'state': state})
    return rooms

def get_theme():
    try:
        return GlobalVar.objects.get(name="admin_theme").value
    except:
        return "blue"

def get_sidebar():
    return get_theme(), get_bookablerooms()

def index(req):
    theme, rooms = get_sidebar()
    return render(req, "Admin/dashboard.html", locals())

from EpiRooms.management.commands import get_planning
@csrf_exempt
def getplanning(req):
    if req.method == "POST":
        r = requests.get('https://intra.epitech.eu/auth-d73b3db1c918b7826c565155d5e65388a2d0f938/planning/load?format=json')
        planning = r.json()
        now = timezone.now()
        week = []
        try:
            city = GlobalVar.objects.get(name="City").value
        except:
            return Log(level=2, log_from="Get Planning", log_message="GlobalVar \"City\" not found!").save()
        for evt in planning:
            if "acti_title" in evt and "room" in evt and evt["room"] and "code" in evt["room"] and evt["room"]["code"].startswith(city):
                week.append(evt)
        week = sorted(week, key=lambda k: k['start'], reverse=False)
        Booking.objects.filter(user=None).delete()
        for evt in week:
            room = None
            try:
                room = Room.objects.get(name__iexact=evt['room']["code"].split('/')[-1])
            except:
                Log(level=2, log_from="Get Planning - Get room", log_message="Room " + evt['room']["code"].split('/')[-1] + " not found for event:\n" + json.dumps(evt, indent=4, separators=(',', ': '))).save()
            if room:
                try:
                    Booking(room=room, description=evt["acti_title"], start=datetime.strptime(evt["start"], "%Y-%m-%d %H:%M:%S"), end=datetime.strptime(evt["end"], "%Y-%m-%d %H:%M:%S")).save()
                except:
                    Log(level=2, log_from="Get Planning - save Event", log_message="Event error for event:\n" + json.dumps(evt, indent=4, separators=(',', ': '))).save()
        return JsonResponse({})
    theme, rooms = get_sidebar()
    return render(req, "Admin/sync.html", locals())

def planning(req):
    now = timezone.now()
    theme, rooms = get_sidebar()
    events = []
    start = now - timedelta(days=1)
    start = start.strftime("%Y-%m-%d %H:%M:%S")
    end = now + timedelta(days=15 - now.weekday() - 1)
    end = end.strftime("%Y-%m-%d")
    for evt in Booking.objects.filter(end__gt=now):
        events.append({
            'id': evt.id,
            'title': (evt.description if evt.description else evt.user.name) + " : " + evt.room.name,
            'room': evt.room.name,
            'description': (evt.description if evt.description else evt.user.name),
            'start': evt.start.strftime("%Y-%m-%d %H:%M"),
            'end': evt.end.strftime("%Y-%m-%d %H:%M"),
            'backgroundColor': "#3c8dbc" if evt.description else "#605ca8"
        })
    return render(req, "Admin/planning.html", locals())

def rooms(req, room_id):
    try:
        room = Room.objects.get(id=room_id)
    except:
        return redirect('/admin')
    now = timezone.now()
    theme, rooms = get_sidebar()
    events = []
    start = now - timedelta(days=1)
    start = start.strftime("%Y-%m-%d %H:%M:%S")
    end = now + timedelta(days=15 - now.weekday() - 1)
    end = end.strftime("%Y-%m-%d")
    for evt in Booking.objects.filter(end__gt=now, room__id=room_id):
        events.append({
            'id': evt.id,
            'title': (evt.description if evt.description else evt.user.name) + " : " + evt.room.name,
            'room': evt.room.name,
            'description': (evt.description if evt.description else evt.user.name),
            'start': evt.start.strftime("%Y-%m-%d %H:%M"),
            'end': evt.end.strftime("%Y-%m-%d %H:%M"),
            'backgroundColor': "#605ca8" if evt.description else "#605ca8",
        })
    return render(req, "Admin/room.html", locals())

def users(req):
    theme, rooms = get_sidebar()
    return render(req, "Admin/users.html", locals())

def logs(req):
    theme, rooms = get_sidebar()
    return render(req, "Admin/logs.html", locals())

@csrf_exempt
def cmd(req):
    if req.method == "POST":
        ret = run(req.POST['cmd'].split(' '), stdout=PIPE, stderr=PIPE, universal_newlines=True)
        return JsonResponse({'ret': str(ret.stdout)})
    return redirect("/")

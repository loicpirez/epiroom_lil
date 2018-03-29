from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.db.models import Q
from datetime import datetime, timedelta
import json

from .models import *

# Create your views here.
def rooms(req, room=None):
    if not room:
        rooms = Room.objects.all()
    else:
        try:
            rooms = Room.objects.filter(id=room)
        except:
            rooms = Room.objects.filter(name__iexact=room)
    return JsonResponse(list(rooms.values('id', 'name', 'show', 'bookable', 'svg_ids')), safe=False)

def users(req, user=None):
    if not user:
        users = User.objects.all()
        return JsonResponse(list(users.values('id', 'name', 'email', 'access_token', 'token_id', 'last_login')), safe=False)
    else:
        try:
            users = User.objects.filter(id=user)
        except:
            users = User.objects.filter(name__iexact=user) | User.objects.filter(email__iexact=user)
        if not users:
            return JsonResponse({}, safe=False)
        return JsonResponse(list(users.values('id', 'name', 'email', 'access_token', 'token_id', 'last_login'))[0], safe=False)

def bookings(req, id=None):
    if not id:
        bookings = Booking.objects.all()
        return JsonResponse(list(bookings.values('id', 'room__svg_ids', 'user', 'start', 'end')), safe=False)
    else:
        bookings = Booking.objects.filter(id=id)
        return JsonResponse(list(bookings.values('id', 'room__svg_ids', 'user', 'start', 'end'))[0], safe=False)

def get_dic_value(dic, item):
    if not dic:
        return 0
    return dic[item]

from django.views.decorators.cache import cache_page

@cache_page(0.5)
def dispo(req, room=None):
    now = timezone.now()
    rooms = Room.objects.filter(show=True)
    ret = {}
    for room in rooms:
        svg_room = room.svg_ids.split(';')
        for r in svg_room:
            if not r in ret:
                ret[r] = None
            tomorrow = datetime(year=now.year, month=now.month, day=now.day + 1)
            acti = Booking.objects.filter(room__svg_ids__icontains=r, end__gt=now, start__lt=tomorrow).order_by('start')
            if acti:
                taken = 1 if now >= acti[0].start else 0
                if not taken:
                    taken = 0.5 if now + timedelta(hours=1) >= acti[0].start else 0
                if acti:
                    time = acti[0].end - now if taken == 1 else acti[0].start - now
                    end_time = acti[0].end if taken == 1 else acti[0].start - timedelta(hours=1)
                    percent = int(time.total_seconds() / 60) / 60 * 100
                    if taken == 1:
                        percent = 100 - int(time.total_seconds() / (acti[0].end.timestamp() - acti[0].start.timestamp()) * 100)
                    elif taken == 0.5:
                        percent = int(time.total_seconds() / 60) / 60 * 100
                    ret[r] = {
                        'taken': taken,
                        'time': str(time),
                        'course': list(acti.values('id', 'user', 'description', 'start', 'end'))[0],
                        'percent': percent
                    }
    sorted_room = sorted(ret, key=lambda d:get_dic_value(ret[d], 'taken'), reverse=False)
    rooms = {}
    for room in sorted_room:
        rooms[room] = ret[room]
    return JsonResponse({'time_now': now, 'rooms': rooms}, safe=False)

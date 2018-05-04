from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from datetime import datetime, timedelta
import requests, json

from Api.models import Booking, Room
from EpiRooms.models import Log, GlobalVar

from django.db import transaction

class Command(BaseCommand):
    @transaction.atomic
    def handle(self, *args, **options):
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
        Booking.objects.all().delete()
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
        Log(level=0, log_from="Get Planning", log_message="Planning refresh done").save()

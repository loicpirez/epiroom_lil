from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from datetime import datetime, timedelta
import requests, json, os

from Api.models import Booking, Room
from EpiRooms.models import Log, GlobalVar

from django.db import transaction

autologin = os.environ['INTRA_AUTH']

class Command(BaseCommand):
    @transaction.atomic
    def handle(self, *args, **options):
        day = timezone.now().date()
        start = "%d-%d-%d" % (day.year, day.month, day.day)
        tomorrow = timezone.now().date() + timedelta(days=1)
        end = "%d-%d-%d" % (tomorrow.year, tomorrow.month, tomorrow.day)
        r = requests.get('https://intra.epitech.eu/' + autologin + '/planning/load?format=json&start=' + start + '&end=' + end, cookies={"language": "fr"})
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
        Booking.objects.filter(manual=False).delete()
        for evt in week:
            room = None
            try:
                room = Room.objects.get(name__iexact=evt['room']["code"].split('/')[-1])
            except:
                Log(level=2, log_from="Get Planning - Get room", log_message="Room " + evt['room']["code"].split('/')[-1] + " not found for event:\n" + json.dumps(evt, indent=4, separators=(',', ': '))).save()
            if room:
                try:
                    nb_student = 0
                    if evt["type_code"] == "rdv":
                        nb_student = evt["nb_group"]
                    else:
                        nb_student = evt["total_students_registered"]
                    print(evt["acti_title"])
                    Booking(room=room, description=evt["titlemodule"].split('-')[0] + " - " + evt["acti_title"], start=datetime.strptime(evt["start"], "%Y-%m-%d %H:%M:%S"), end=datetime.strptime(evt["end"], "%Y-%m-%d %H:%M:%S"), registered=nb_student).save()
                except:
                    Log(level=2, log_from="Get Planning - save Event", log_message="Event error for event:\n" + json.dumps(evt, indent=4, separators=(',', ': '))).save()
        Log(level=0, log_from="Get Planning", log_message="Planning refresh done").save()        

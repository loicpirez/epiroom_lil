from django.db import models
from django.utils import timezone

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=128)
    email = models.CharField(max_length=128)
    access_token = models.CharField(max_length=2048, blank=True)
    token_id = models.CharField(max_length=2048, blank=True)
    last_login = models.DateTimeField(default=timezone.now)
    user_type = models.IntegerField(default=0)

    def __str__(self):
        return self.email + " " + str(self.last_login)

class Room(models.Model):
    name = models.CharField(max_length=128)
    show = models.BooleanField(default=True)
    bookable = models.BooleanField(default=True)
    svg_ids = models.CharField(max_length=128, null=True, blank=True)

    def __str__(self):
        return self.name + (" | Show" if self.show else "") + (" | Bookable" if self.bookable else "")

class Booking(models.Model):
    room = models.ForeignKey('Room', on_delete=models.CASCADE)
    user = models.ForeignKey('User', blank=True, null=True, on_delete=models.CASCADE)
    description = models.CharField(max_length=128, blank=True, null=True)
    start = models.DateTimeField(default=timezone.now)
    end = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.room.name + " " + (self.user.name if self.user else self.description) + " " + str(self.start) + " " + str(self.end)

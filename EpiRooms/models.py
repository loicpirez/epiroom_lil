from django.db import models
from django.utils import timezone

# Create your models here.
class Log(models.Model):
    LEVELS = (
        (0, 'Info'),
        (1, 'Warning'),
        (2, 'Danger'),
    )
    level = models.IntegerField(default=0, choices=LEVELS)
    log_from = models.CharField(max_length=128)
    log_message = models.TextField()
    datetime = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.datetime.strftime("%d/%m/%Y %H:%M:%S") + " : " + str(self.level) + ' : ' + self.log_from + ' : ' + self.log_message

class GlobalVar(models.Model):
    name = models.CharField(max_length=128)
    value = models.CharField(blank=True, null=True, max_length=128)

    def __str__(self):
        return self.value

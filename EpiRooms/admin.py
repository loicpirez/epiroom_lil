from django.contrib import admin
from .models import *

class LogAdmin(admin.ModelAdmin):
    def get_message(self, obj):
        return obj.log_message[:20]
    def get_time(self, obj):
        return obj.datetime.strftime("%d/%m/%Y %H:%M:%S")
    list_display = ('get_time', 'level', 'log_from', 'get_message')

class GlobalVarAdmin(admin.ModelAdmin):
    list_display = ('name', 'value')

# Register your models here.
admin.site.register(Log, LogAdmin)
admin.site.register(GlobalVar, GlobalVarAdmin)

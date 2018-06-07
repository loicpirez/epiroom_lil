from django.contrib import admin
from .models import *

class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'last_login')
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'show', 'bookable', 'seats')
class BookingAdmin(admin.ModelAdmin):
    def get_room(self, obj):
        return obj.room.name
    def get_user(self, obj):
        return obj.room.name
    list_display = ('get_room', 'get_user', 'start', 'end', 'description')

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(Booking, BookingAdmin)

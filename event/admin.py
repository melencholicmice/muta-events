from django.contrib import admin

from .models import Event , EventAttendee

admin.site.register(Event)
admin.site.register(EventAttendee)


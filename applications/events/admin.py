from django.contrib import admin

from .models import Event, Event_Detail, Participants

admin.site.register(Event)
admin.site.register(Event_Detail)
admin.site.register(Participants)

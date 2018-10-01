"""
    Profile administration
"""
from django.contrib import admin
from seven23.models.events.models import Event, Attendee, EventToken

admin.site.register(Event)
admin.site.register(Attendee)
admin.site.register(EventToken)

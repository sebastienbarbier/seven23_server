"""
    Serializer for Categories module
"""
from rest_framework import serializers
from seven23.models.accounts.models import Account
from seven23.models.events.models import Event, Attendee

class AttendeeSerializer(serializers.HyperlinkedModelSerializer):
    """
        Serialize Attendee model
    """
    event = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all(), required=False)

    class Meta:
        model = Attendee
        fields = ('id', 'event', 'fullname', 'email')

class EventSerializer(serializers.HyperlinkedModelSerializer):
    """
        Serialize Event model
    """
    account = serializers.PrimaryKeyRelatedField(queryset=Account.objects.all())
    attendees = AttendeeSerializer(many=True, required=False)

    class Meta:
        model = Event
        fields = ('id', 'account', 'title', 'date_begin', 'date_end', 'archived', 'attendees')

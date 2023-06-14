"""
    Serializer for Currency module
"""
from rest_framework import serializers
from seven23.models.profile.models import Profile

class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Profile
        fields = ['avatar', 'auto_sync', 'key_verified', 'social_networks']


class DatetimeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Profile
        fields = ['valid_until']
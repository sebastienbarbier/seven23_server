"""
    Serializer for Currency module
"""
from rest_framework import serializers
from seven23.models.profile.models import Profile

class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    """
        Serialize Currency model
    """
    class Meta:
        model = Profile
        fields = ['avatar', 'social_networks']
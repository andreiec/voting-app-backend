from rest_framework import serializers
from .models import Profile, Group


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"


class ProfileSerializer(serializers.ModelSerializer):
    group = serializers.CharField(source='get_group_id')
    class Meta:
        model = Profile
        fields = "__all__"

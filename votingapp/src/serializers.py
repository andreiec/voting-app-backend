from pyexpat import model
from django.forms import fields
from rest_framework import serializers
from .models import Profile, Group


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"


class GroupIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ["_id"]


class ProfileSerializer(serializers.ModelSerializer):
    group = GroupIdSerializer(many=False, read_only=True)
    class Meta:
        model = Profile
        fields = "__all__"

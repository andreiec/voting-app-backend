from rest_framework import serializers
from .models import User, Group


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    group = serializers.CharField(source='get_group_id')
    class Meta:
        model = User
        fields = "__all__"

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .serializers import UserSerializer, GroupSerializer
from .models import User, Group

from bson import ObjectId


@api_view(['GET'])
def baseResponse(request):
    return Response()


# USERS

@api_view(['GET'])
def getUsers(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return(Response(serializer.data))


@api_view(['GET'])
def getUser(request, pk):
    user = User.objects.get(_id=ObjectId(pk))
    serializer = UserSerializer(user, many=False)
    return(Response(serializer.data))


# GROUPS

@api_view(['GET'])
def getGroups(request):
    groups = Group.objects.all()
    serializer = GroupSerializer(groups, many=True)
    return(Response(serializer.data))


@api_view(['GET'])
def getGroup(request, pk):
    groups = Group.objects.get(_id=ObjectId(pk))
    serializer = GroupSerializer(groups, many=False)
    return(Response(serializer.data))


@api_view(['GET'])
def getAllUsersFromGroup(request, pk):
    profiles = User.objects.filter(group___id=ObjectId(pk))
    serializer = UserSerializer(profiles, many=True)
    return(Response(serializer.data))
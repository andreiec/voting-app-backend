from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .serializers import UserSerializer, GroupSerializer
from .models import User, Group

from bson import ObjectId


@api_view(['GET'])
def baseResponse(request):
    return Response()



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


# @api_view(['GET'])
# def getAllProfilesFromGroup(request, pk):
#     profiles = Profile.objects.filter(group___id=ObjectId(pk))
#     serializer = ProfileSerializer(profiles, many=True)
#     return(Response(serializer.data))
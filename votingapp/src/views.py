from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from bson import ObjectId

from .serializers import ProfileSerializer
from .models import Profile



@api_view(['GET'])
def baseResponse(request):
    return Response()


@api_view(['GET'])
def getProfiles(request):
    profiles = Profile.objects.all()
    serializer = ProfileSerializer(profiles, many=True)
    return(Response(serializer.data))


@api_view(['GET'])
def getProfile(request, pk):
    profiles = Profile.objects.get(_id=ObjectId(pk))
    serializer = ProfileSerializer(profiles, many=False)
    return(Response(serializer.data))

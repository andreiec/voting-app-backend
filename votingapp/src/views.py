from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .serializers import UserSerializer, GroupSerializer
from .models import User, Group
from .views_utils import createUser

from bson import ObjectId


@api_view(['GET'])
def baseResponse(request):
    return Response()


# USERS

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def getUsers(request):

    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return(Response(serializer.data))

    elif request.method == 'POST':
        return createUser(request)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUser(request, pk):
    user = User.objects.get(_id=ObjectId(pk))
    serializer = UserSerializer(user, many=False)
    return(Response(serializer.data))


# GROUPS

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getGroups(request):
    groups = Group.objects.all()
    serializer = GroupSerializer(groups, many=True)
    return(Response(serializer.data))


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getGroup(request, pk):
    groups = Group.objects.get(_id=ObjectId(pk))
    serializer = GroupSerializer(groups, many=False)
    return(Response(serializer.data))


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getAllUsersFromGroup(request, pk):
    profiles = User.objects.filter(group___id=ObjectId(pk))
    serializer = UserSerializer(profiles, many=True)
    return(Response(serializer.data))
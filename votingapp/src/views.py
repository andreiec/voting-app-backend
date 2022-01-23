from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import ViewSet

from django.shortcuts import get_object_or_404

from .serializers import UserSerializer, GroupSerializer
from .models import User, Group
from .views_utils import createUser

from bson import ObjectId
from permissions import UsersPermissions


@api_view(['GET'])
def baseResponse(request):
    return Response()


# User CRUD endpoints done with ViewSet
class UserSet(ViewSet):
    permission_classes = [UsersPermissions]
    queryset = User.objects.all()


    def list(self, request):
        serializer = UserSerializer(self.queryset, many=True)
        return(Response(serializer.data))


    def create(self, request):
        return createUser(request)


    def retrieve(self, request, pk=None):
        user = get_object_or_404(self.queryset, pk=ObjectId(pk))
        serializer = UserSerializer(user, many=False)
        return(Response(serializer.data))


    def update(self, request, pk=None):
        pass


    def partial_update(self, request, pk=None):
        pass


    def destroy(self, request, pk=None):
        user = get_object_or_404(self.queryset, pk=ObjectId(pk))
        user.delete()
        return(Response({
            'detail': 'User deleted.',
        }, status=status.HTTP_200_OK))


# ENDPOINTS FOR GROUPS

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
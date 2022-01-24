from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import ViewSet

from django.shortcuts import get_object_or_404

from .serializers import UserSerializer, GroupSerializer
from .models import User, Group
from .views_utils import createUser, createGroup

from bson import ObjectId
from permissions import UsersPermissions


@api_view(['GET'])
def baseResponse(request):
    return Response()


# User create, read, update, delete endpoints 
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
        user = get_object_or_404(self.queryset, pk=ObjectId(pk))
        serializer = UserSerializer(user, data=request.data, partial=True)

        # Check if request wants to modify _id
        if request.data.get('_id', False):
            return(Response({
            'detail': 'Cannot change id.',
        }, status=status.HTTP_400_BAD_REQUEST))

        # If serializer is valid
        if serializer.is_valid():
            serializer.save()
            return(Response({
                'detail': 'User updated.',
            }, status=status.HTTP_202_ACCEPTED))

        # Serializer was not valid
        return(Response({
            'detail': 'Bad request.',
        }, status=status.HTTP_400_BAD_REQUEST))


    # Who uses PATCH request anyways?
    def partial_update(self, request, pk=None):
        return(Response({
            'detail': 'Bad request.',
        }, status=status.HTTP_400_BAD_REQUEST))


    def destroy(self, request, pk=None):
        user = get_object_or_404(self.queryset, pk=ObjectId(pk))
        user.delete()
        return(Response({
            'detail': 'User deleted.',
        }, status=status.HTTP_200_OK))


# Group create, read, update, delete endpoints 
class GroupSet(ViewSet):
    permission_classes = [IsAdminUser]
    queryset = Group.objects.all()

    def list(self, request):
        serializer = GroupSerializer(self.queryset, many=True)
        return(Response(serializer.data))


    def create(self, request):
        return createGroup(request)


    def retrieve(self, request, pk=None):
        group = get_object_or_404(self.queryset, pk=ObjectId(pk))
        serializer = GroupSerializer(group, many=False)
        return(Response(serializer.data))


    def update(self, request, pk=None):
        group = get_object_or_404(self.queryset, pk=ObjectId(pk))
        serializer = GroupSerializer(group, data=request.data, partial=True)

        # Check if request wants to modify _id
        if request.data.get('_id', False):
            return(Response({
            'detail': 'Cannot change id.',
        }, status=status.HTTP_400_BAD_REQUEST))

        # If serializer is valid
        if serializer.is_valid():
            serializer.save()
            return(Response({
                'detail': 'Group updated.',
            }, status=status.HTTP_202_ACCEPTED))

        # Serializer was not valid
        return(Response({
            'detail': 'Bad request.',
        }, status=status.HTTP_400_BAD_REQUEST))


    # Who uses PATCH request anyways?
    def partial_update(self, request, pk=None):
        return(Response({
            'detail': 'Bad request.',
        }, status=status.HTTP_400_BAD_REQUEST))


    def destroy(self, request, pk=None):
        group = get_object_or_404(self.queryset, pk=ObjectId(pk))
        group.delete()
        return(Response({
            'detail': 'Group deleted.',
        }, status=status.HTTP_200_OK))



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getAllUsersFromGroup(request, pk):
    profiles = User.objects.filter(group___id=ObjectId(pk))
    serializer = UserSerializer(profiles, many=True)
    return(Response(serializer.data))
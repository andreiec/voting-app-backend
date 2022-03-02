from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import ViewSet
from rest_framework.authentication import TokenAuthentication

from django.shortcuts import get_object_or_404

from .serializers import SingleElectionSerializer, MultipleElectionSerializer, UserSerializer, GroupSerializer
from .models import Election, User, Group
from .views_utils import createUser, createGroup, createElection

from permissions import UsersPermissions, ElectionsPermissions, GroupsPermissions
import uuid


@api_view(['GET'])
def baseResponse(request):
    return Response()


# User create, read, update, delete endpoints 
class UserSet(ViewSet):
    permission_classes = [UsersPermissions]
    # authentication_classes = [TokenAuthentication]
    # queryset = User.objects.all()


    def list(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return(Response(serializer.data))


    def create(self, request):
        return createUser(request)


    def retrieve(self, request, pk=None):
        # Check if id is a valid uuid
        try:
            uuid.UUID(pk)
        except:
            return(Response({
                'detail': 'Bad request.',
            }, status=status.HTTP_400_BAD_REQUEST))

        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = UserSerializer(user, many=False)
        return(Response(serializer.data))


    def update(self, request, pk=None):
        # Check if id is a valid uuid
        try:
            uuid.UUID(pk)
        except:
            return(Response({
                'detail': 'Bad request.',
            }, status=status.HTTP_400_BAD_REQUEST))

        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = UserSerializer(user, data=request.data, partial=True)

        # Check if request wants to modify id
        if request.data.get('id', False):
            return(Response({
            'detail': 'Cannot change id.',
        }, status=status.HTTP_400_BAD_REQUEST))

        # If serializer is valid
        if serializer.is_valid():
            serializer.save()
            return(Response({
                'detail': 'User updated.',
            }, status=status.HTTP_200_OK))

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
        # Check if id is a valid uuid
        try:
            uuid.UUID(pk)
        except:
            return(Response({
                'detail': 'Bad request.',
            }, status=status.HTTP_400_BAD_REQUEST))

        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        user.delete()
        return(Response({
            'detail': 'User deleted.',
        }, status=status.HTTP_200_OK))


# Group create, read, update, delete endpoints 
class GroupSet(ViewSet):
    permission_classes = [GroupsPermissions]
    # authentication_classes = [TokenAuthentication]
    # queryset = Group.objects.all()

    def list(self, request):
        queryset = Group.objects.all()
        serializer = GroupSerializer(queryset, many=True)
        return(Response(serializer.data))


    def create(self, request):
        return createGroup(request)


    def retrieve(self, request, pk=None):
        # Check if id is a valid uuid
        try:
            uuid.UUID(pk)
        except:
            return(Response({
                'detail': 'Bad request.',
            }, status=status.HTTP_400_BAD_REQUEST))

        queryset = Group.objects.all()
        group = get_object_or_404(queryset, pk=pk)
        serializer = GroupSerializer(group, many=False)
        return(Response(serializer.data))


    def update(self, request, pk=None):
        # Check if id is a valid uuid
        try:
            uuid.UUID(pk)
        except:
            return(Response({
                'detail': 'Bad request.',
            }, status=status.HTTP_400_BAD_REQUEST))

        queryset = Group.objects.all()
        group = get_object_or_404(queryset, pk=pk)
        serializer = GroupSerializer(group, data=request.data, partial=True)

        # Check if request wants to modify id
        if request.data.get('id', False):
            return(Response({
            'detail': 'Cannot change id.',
        }, status=status.HTTP_400_BAD_REQUEST))

        # If serializer is valid
        if serializer.is_valid():
            serializer.save()
            return(Response({
                'detail': 'Group updated.',
            }, status=status.HTTP_200_OK))

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
        # Check if id is a valid uuid
        try:
            uuid.UUID(pk)
        except:
            return(Response({
                'detail': 'Bad request.',
            }, status=status.HTTP_400_BAD_REQUEST))

        queryset = Group.objects.all()
        group = get_object_or_404(queryset, pk=pk)
        group.delete()
        return(Response({
            'detail': 'Group deleted.',
        }, status=status.HTTP_200_OK))



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getAllUsersFromGroup(request, pk):
    # Check if id is a valid uuid
    try:
        uuid.UUID(pk)
    except:
        return(Response({
            'detail': 'Bad request.',
        }, status=status.HTTP_400_BAD_REQUEST))

    profiles = User.objects.filter(group__id=pk)
    serializer = UserSerializer(profiles, many=True)
    return(Response(serializer.data))


class ElectionSet(ViewSet):
    permission_classes = [ElectionsPermissions]
    # authentication_classes = [TokenAuthentication]
    # queryset = Election.objects.all()


    def list(self, request):
        queryset = Election.objects.all()
        serializer = MultipleElectionSerializer(queryset, many=True)
        return(Response(serializer.data))


    def create(self, request):
        return createElection(request)


    def retrieve(self, request, pk=None):
        # Check if id is a valid uuid
        try:
            uuid.UUID(pk)
        except:
            return(Response({
                'detail': 'Bad request.',
            }, status=status.HTTP_400_BAD_REQUEST))

        queryset = Election.objects.all()
        election = get_object_or_404(queryset, pk=pk)
        serializer = SingleElectionSerializer(election, many=False)
        return(Response(serializer.data))


    def update(self, request, pk=None):
        pass


    # Who uses PATCH request anyways?
    def partial_update(self, request, pk=None):
        return(Response({
            'detail': 'Bad request.',
        }, status=status.HTTP_400_BAD_REQUEST))


    def destroy(self, request, pk=None):
        # Check if id is a valid uuid
        try:
            uuid.UUID(pk)
        except:
            return(Response({
                'detail': 'Bad request.',
            }, status=status.HTTP_400_BAD_REQUEST))

        queryset = Election.objects.all()
        election = get_object_or_404(queryset, pk=pk)
        election.delete()
        return(Response({
            'detail': 'Election deleted.',
        }, status=status.HTTP_200_OK))


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getAllElectionsFromUser(request, pk):
    # Check if id is a valid uuid
    try:
        uuid.UUID(pk)
    except:
        return(Response({
            'detail': 'Bad request.',
        }, status=status.HTTP_400_BAD_REQUEST))

    user = get_object_or_404(User.objects.all(), pk=pk)
    elections = Election.objects.filter(groups__in=[user.group])
    serializer = MultipleElectionSerializer(elections, many=True)
    return(Response(serializer.data))
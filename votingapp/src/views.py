from django.http import Http404, HttpResponseNotFound
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import ViewSet
from rest_framework.authentication import TokenAuthentication

from django.shortcuts import get_object_or_404

from .serializers import SingleElectionSerializer, MultipleElectionSerializer, UserSerializer, GroupSerializer
from .models import Election, Option, User, Group, Vote
from .views_utils import createUser, createGroup, createElection, validateUUID

from permissions import UsersPermissions, ElectionsPermissions, GroupsPermissions
import uuid, json


@api_view(['GET'])
def baseResponse(request):
    return Response()


# User create, read, update, delete endpoints 
class UserSet(ViewSet):
    permission_classes = [UsersPermissions]


    def list(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return(Response(serializer.data))


    def create(self, request):
        return createUser(request)


    def retrieve(self, request, pk=None):
        if not validateUUID(pk):
            return HttpResponseNotFound("Not found.")

        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = UserSerializer(user, many=False)
        return(Response(serializer.data))


    def update(self, request, pk=None):
        if not validateUUID(pk):
            return HttpResponseNotFound("Not found.")

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
        if not validateUUID(pk):
            return HttpResponseNotFound("Not found.")

        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        user.delete()
        return(Response({
            'detail': 'User deleted.',
        }, status=status.HTTP_200_OK))


# Group create, read, update, delete endpoints 
class GroupSet(ViewSet):
    permission_classes = [GroupsPermissions]


    def list(self, request):
        queryset = Group.objects.all()
        serializer = GroupSerializer(queryset, many=True)
        return(Response(serializer.data))


    def create(self, request):
        return createGroup(request)


    def retrieve(self, request, pk=None):
        if not validateUUID(pk):
            return HttpResponseNotFound("Not found.")

        queryset = Group.objects.all()
        group = get_object_or_404(queryset, pk=pk)
        serializer = GroupSerializer(group, many=False)
        return(Response(serializer.data))


    def update(self, request, pk=None):
        if not validateUUID(pk):
            return HttpResponseNotFound("Not found.")

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
        if not validateUUID(pk):
            return HttpResponseNotFound("Not found.")

        queryset = Group.objects.all()
        group = get_object_or_404(queryset, pk=pk)
        group.delete()
        return(Response({
            'detail': 'Group deleted.',
        }, status=status.HTTP_200_OK))


class ElectionSet(ViewSet):
    permission_classes = [ElectionsPermissions]


    def list(self, request):
        queryset = Election.objects.all()
        serializer = MultipleElectionSerializer(queryset, many=True)
        return(Response(serializer.data))


    def create(self, request):
        return createElection(request)


    def retrieve(self, request, pk=None):
        if not validateUUID(pk):
            return HttpResponseNotFound("Not found.")

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
        if not validateUUID(pk):
            return HttpResponseNotFound("Not found.")

        queryset = Election.objects.all()
        election = get_object_or_404(queryset, pk=pk)
        election.delete()
        return(Response({
            'detail': 'Election deleted.',
        }, status=status.HTTP_200_OK))


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getAllUsersFromGroup(request, pk):
    if not validateUUID(pk):
        return HttpResponseNotFound("Not found.")

    profiles = User.objects.filter(group__id=pk)
    serializer = UserSerializer(profiles, many=True)
    return(Response(serializer.data))


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getAllElectionsFromUser(request, pk):
    if not validateUUID(pk):
        return HttpResponseNotFound("Not found.")

    user = get_object_or_404(User.objects.all(), pk=pk)
    elections = Election.objects.filter(groups__in=[user.group])
    serializer = MultipleElectionSerializer(elections, many=True)
    return(Response(serializer.data))


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submitVotes(request, pk):
    election_data = request.data
    election_votes = election_data['votes']
    user_id = election_data['user_id']
    user = get_object_or_404(User.objects.all(), pk=user_id)

    # UUID Validation
    if not validateUUID(user_id) or not validateUUID(pk):
        return(Response({
            'detail': 'Bad request.',
        }, status=status.HTTP_400_BAD_REQUEST))

    # UUID Validation
    for question_id in election_votes:
        options = election_votes[question_id]

        # Validate question id
        if not validateUUID(question_id):
            return(Response({
                'detail': 'Bad request.',
            }, status=status.HTTP_400_BAD_REQUEST))

        # Validate option 
        if type(options) is str:
            if not validateUUID(options):
                return(Response({
                    'detail': 'Bad request.',
                }, status=status.HTTP_400_BAD_REQUEST))
                
        elif type(options) is list:
            for option in options:
                if not validateUUID(option):
                    return(Response({
                        'detail': 'Bad request.',
                    }, status=status.HTTP_400_BAD_REQUEST))
        else:
            return(Response({
                'detail': 'Bad request.',
            }, status=status.HTTP_400_BAD_REQUEST))

    # Store all votes in a list to do a bulk create
    votes_to_bulk_create = []
    bulk_create_is_valid = True

    # Adding votes to database
    for question_id in election_votes:
        # If question was single select (returned option would be a single str)
        if type(election_votes[question_id]) is str:
            option = Option.objects.get(pk=election_votes[question_id])

            # If an option was not found in the db don't validate
            if not option:
                bulk_create_is_valid = False
                break

            vote = Vote(user=user, option=option)
            votes_to_bulk_create.append(vote)

        # If question was multiple select (returned option would be a list of str)
        elif type(election_votes[question_id]) is list:
            for option_id in election_votes[question_id]:
                option = Option.objects.get(pk=option_id)

                # If an option was not found in the db don't validate
                if not option:
                    bulk_create_is_valid = False
                    break

                vote = Vote(user=user, option=option)
                votes_to_bulk_create.append(vote)

    # If all validation is met, bulk create
    if bulk_create_is_valid:
        Vote.objects.bulk_create(votes_to_bulk_create)
    else:
        return(Response({
            'detail': 'Bad request.',
        }, status=status.HTTP_400_BAD_REQUEST))

    return(Response({'detail' : 'Created.',}, status=status.HTTP_201_CREATED))

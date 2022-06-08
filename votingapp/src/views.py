from re import M
from django.http import Http404, HttpResponseNotFound
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import ViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework.renderers import JSONRenderer

from django.shortcuts import get_object_or_404

from .serializers import ClosedElectionSerializer, SingleElectionSerializer, MultipleElectionSerializer, SubmissionSerializer, UserSerializer, GroupSerializer, VoteSerializer
from .models import ClosedElection, Election, Option, User, Group, Vote, Submission
from .views_utils import createUser, createGroup, createElection, validateUUID, checkIfActiveVotes

from permissions import UsersPermissions, ElectionsPermissions, GroupsPermissions


@api_view(['GET'])
def baseResponse(request):
    return Response()


# User create, read, update, delete endpoints 
class UserSet(ViewSet):
    permission_classes = [UsersPermissions]


    def list(self, request):
        queryset = User.objects.order_by('last_name', 'first_name')
        serializer = UserSerializer(queryset, many=True)
        return(Response(serializer.data))


    def create(self, request):
        if checkIfActiveVotes():
            return(Response({
                'detail': 'Cannot change while active votes.'
            }, status=status.HTTP_409_CONFLICT))

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
        
        if checkIfActiveVotes():
            return(Response({
                'detail': 'Cannot change while active votes.'
            }, status=status.HTTP_409_CONFLICT))

        data = request.data

        first_name = data.get('first_name', None)
        last_name = data.get('last_name', None)
        email = data.get('email', None)
        is_staff = data.get('is_staff', False)
        group_id = data.get('group', None)

        group = None

        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)

        if group_id:
            group = get_object_or_404(Group.objects.all(), pk=group_id)


        if not first_name or not last_name or not email:
            return(Response({
                'detail': 'Missing data from sender.',
            }, status=status.HTTP_400_BAD_REQUEST))

        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.is_staff = is_staff
        user.is_admin = is_staff
        user.group = group

        user.save()

        return(Response({
            'detail': 'User updated.',
        }, status=status.HTTP_200_OK))



    # Who uses PATCH request anyways?
    def partial_update(self, request, pk=None):
        return(Response({
            'detail': 'Bad request.',
        }, status=status.HTTP_400_BAD_REQUEST))


    def destroy(self, request, pk=None):
        if not validateUUID(pk):
            return HttpResponseNotFound("Not found.")

        if checkIfActiveVotes():
            return(Response({
                'detail': 'Cannot change while active votes.'
            }, status=status.HTTP_409_CONFLICT))        

        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)

        if user.is_superuser:
            return(Response({
                'detail': 'Cannot delete root admin.'
            }, status=status.HTTP_406_NOT_ACCEPTABLE))     

        user.delete()
        return(Response({
            'detail': 'User deleted.',
        }, status=status.HTTP_200_OK))


# Group create, read, update, delete endpoints 
class GroupSet(ViewSet):
    permission_classes = [GroupsPermissions]


    def list(self, request):
        queryset = Group.objects.order_by('name')
        serializer = GroupSerializer(queryset, many=True)
        return(Response(serializer.data))


    def create(self, request):
        if checkIfActiveVotes():
            return(Response({
                'detail': 'Cannot change while active votes.'
            }, status=status.HTTP_409_CONFLICT))    

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

        if checkIfActiveVotes():
            return(Response({
                'detail': 'Cannot change while active votes.'
            }, status=status.HTTP_409_CONFLICT))    

        queryset = Group.objects.all()
        group = get_object_or_404(queryset, pk=pk)
        serializer = GroupSerializer(group, data=request.data, partial=True)

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

        if checkIfActiveVotes():
            return(Response({
                'detail': 'Cannot change while active votes.'
            }, status=status.HTTP_409_CONFLICT))    

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
        if not validateUUID(pk):
            return HttpResponseNotFound("Not found.")

        queryset = Election.objects.all()
        election = get_object_or_404(queryset, pk=pk)
        serializer = SingleElectionSerializer(election, data=request.data, partial=True)

        # If serializer is valid
        if serializer.is_valid():
            serializer.save()
            return(Response({
                'detail': 'Election updated.',
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

        queryset = Election.objects.all()
        election = get_object_or_404(queryset, pk=pk)
        election.delete()
        return(Response({
            'detail': 'Election deleted.',
        }, status=status.HTTP_200_OK))


class ClosedElectionSet(ViewSet):
    permission_classes = [ElectionsPermissions]


    def list(self, request):
        queryset = ClosedElection.objects.all()
        serializer = ClosedElectionSerializer(queryset, many=True)
        return(Response(serializer.data))


    def create(self, request):
        # Cannot create
        return(Response({
            'detail': 'Bad request.',
        }, status=status.HTTP_400_BAD_REQUEST))


    def retrieve(self, request, pk=None):
        if not validateUUID(pk):
            return HttpResponseNotFound("Not found.")

        queryset = ClosedElection.objects.all()
        election = get_object_or_404(queryset, pk=pk)
        serializer = ClosedElectionSerializer(election, many=False)
        return(Response(serializer.data))


    def update(self, request, pk=None):
        # Cannot update
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

        queryset = ClosedElection.objects.all()
        election = get_object_or_404(queryset, pk=pk)
        election.delete()
        return(Response({
            'detail': 'Archived election deleted.',
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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getAllElectionsFromUserCount(request, pk, count):
    if not validateUUID(pk):
        return HttpResponseNotFound("Not found.")

    user = get_object_or_404(User.objects.all(), pk=pk)
    elections = Election.objects.filter(groups__in=[user.group])[:count]
    serializer = MultipleElectionSerializer(elections, many=True)
    return(Response(serializer.data))


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submitVotes(request, pk):
    election_data = request.data
    election_votes = election_data['votes']

    user_id = election_data['user_id']
    election_id = election_data['election_id']

    user = get_object_or_404(User.objects.all(), pk=user_id)
    election = get_object_or_404(Election.objects.all(), pk=election_id)

    # Check if user already voted
    user_has_voted = Submission.objects.filter(user=user_id, election=election_id)
    
    if user_has_voted:
        return(Response({
            'detail': 'User already voted.'
        }, status=status.HTTP_409_CONFLICT))

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

        for option in options:
            if not validateUUID(option):
                return(Response({
                    'detail': 'Bad request.',
                }, status=status.HTTP_400_BAD_REQUEST))

    # Store all votes in a list to do a bulk create
    votes_to_bulk_create = []
    bulk_create_is_valid = True

    # Adding votes to database
    for question_id in election_votes:
        for option_id in election_votes[question_id]:
            option = Option.objects.get(pk=option_id)

            # If an option was not found in the db don't validate
            if not option:
                bulk_create_is_valid = False
                break

            vote = Vote(user=user, option=option, election=election)
            votes_to_bulk_create.append(vote)

    # If all validation is met, bulk create
    if bulk_create_is_valid:
        Vote.objects.bulk_create(votes_to_bulk_create)
        submission = Submission(user=user, election=election)
        submission.save()
    else:
        return(Response({
            'detail': 'Bad request.',
        }, status=status.HTTP_400_BAD_REQUEST))

    return(Response({'detail' : 'Created.',}, status=status.HTTP_201_CREATED))


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getElectionSubmissions(request, pk):
    if not validateUUID(pk):
        return HttpResponseNotFound("Not found.")

    submissions = Submission.objects.filter(election=pk)
    serializer = SubmissionSerializer(submissions, many=True)
    return(Response(serializer.data))


@api_view(['GET'])
def getOptionVotes(request, pk):
    if not validateUUID(pk):
        return HttpResponseNotFound("Not found.")
    
    votes = Vote.objects.filter(option=pk)
    serializer = VoteSerializer(votes, many=True)
    return(Response(serializer.data))


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getActiveElections(request):
    elections = Election.objects.filter(is_active=True)
    serializer = MultipleElectionSerializer(elections, many=True)
    return(Response(serializer.data))


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getInactiveElections(request):
    elections = Election.objects.filter(is_active=False)
    serializer = MultipleElectionSerializer(elections, many=True)
    return(Response(serializer.data))


# Get all groups from election
@api_view(['GET'])
@permission_classes([IsAdminUser])
def getGroupsFromElection(request, pk):
    if not validateUUID(pk):
        return HttpResponseNotFound("Not found.")

    election = get_object_or_404(Election.objects.all(), pk=pk)
    groups = election.groups.all()

    serializer = GroupSerializer(groups, many=True)
    return(Response(serializer.data))


@api_view(['GET'])
@permission_classes([IsAdminUser])
def closeElection(request, pk):
    if not validateUUID(pk):
        return HttpResponseNotFound("Not found.")

    # Get election and groups
    election = get_object_or_404(Election.objects.all(), pk=pk)

    if election.is_archived:
        return(Response({
            'detail': 'Vote already closed.',
        }, status=status.HTTP_400_BAD_REQUEST))

    groups = election.groups.all()

    # Count votes
    votes = Vote.objects.filter(election__id=election.id)
    number_of_submissions = Submission.objects.filter(election__id=election.id).count()

    # Serialize election
    serializer = SingleElectionSerializer(election, many=False).data

    # Count votes and save as follows -> (key) option_id: (value) number of votes for this option
    counted_votes = {}

    for vote in votes:
        option_id = str(vote.option.id)

        if option_id not in counted_votes:
            counted_votes[option_id] = 1
        else:
            counted_votes[option_id] += 1

    # Construct final json
    final_data = {
        'title': serializer.get('title'),
        'description': serializer.get('description'),
        'number_of_polls': serializer.get('number_of_polls'),
        "voting_starts_at": serializer.get('voting_starts_at'),
        "voting_ends_at": serializer.get('voting_ends_at'),
        'submitted_votes': number_of_submissions,
        'questions': [],
        'groups': [{'id': str(group.id), 'name': group.name, 'description': group.description} for group in groups]
    }

    # Iterate each question and create it, iterate each option and count votes
    for question in serializer.get('questions'):
        question_data = {
            'title': question.get('title'),
            'description': question.get('description'),
            "selection_type": question.get("selection_type"),
            "min_selections": question.get('min_selections'),
            "max_selections": question.get('max_selections'),
            "order": question.get('order'),
            'options': []
        }

        for option in question.get('options'):
            option_data = {
                "value": option.get('value'),
                "order": option.get('order')
            }

            if option.get('id') in counted_votes:
                option_data['vote_count'] = counted_votes[option.get('id')]
            else:
                option_data['vote_count'] = 0
            
            question_data['options'].append(option_data)

        final_data['questions'].append(question_data)

    closed_election = ClosedElection(election=election, data=final_data)
    closed_election.save()

    election.is_active = False
    election.is_archived = True
    election.accepts_votes = False
    election.save()

    return(Response({
        'detail': 'Vote closed.',
        'vote_id': str(closed_election.id),
    }, status=status.HTTP_200_OK))


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def changeUserPassword(request, pk):
    if not validateUUID(pk):
        return HttpResponseNotFound("Not found.")
    

    new_password = request.data['password']

    user = get_object_or_404(User.objects.all(), pk=pk)
    user.set_password(new_password)
    user.save()

    return(Response({
        'detail': 'Password changed.',
    }, status=status.HTTP_200_OK))
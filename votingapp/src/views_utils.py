from datetime import datetime
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from src.models import User, Group, Election, Question, Option
from src.serializers import UserSerializer, GroupSerializer, SingleElectionSerializer


import uuid

# Helper function to validate uuid
def validateUUID(id):
    try:
        uuid.UUID(id)
        return True
    except:
        return False


# Create user from post request
def createUser(request):

    # Get data from post request
    data = request.data
    email = data.get('email', None)
    password = data.get('password', None)
    group = data.get('group', None)
    is_staff = data.get('is_staff', False)

    # Check if data contains email
    if not email:
        return(Response({
            'detail': 'Missing data from sender.',
        }, status=status.HTTP_400_BAD_REQUEST))

    # If not password, create random
    # if not password:
    #    password = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(8))

    # Check if mail already exists in db
    if User.objects.filter(email=email).exists():
        return(Response({
            'detail': 'Mail already exists.',
        }, status=status.HTTP_400_BAD_REQUEST))

    # Create user dict with data for serialization
    user_data = {
        'email': email,
        'first_name': data.get('first_name', ""),
        'last_name': data.get('last_name', ""),
        'date_joined': str(timezone.now()),
        'last_login': str(timezone.now()),
        'is_staff': data.get('is_staff', False),
    }

    # Get group if exists
    if group:
        try:
            group_pk = uuid.UUID(group, version=4)
        except:
            return(Response({
                'detail': 'Bad group id.',
            }, status=status.HTTP_400_BAD_REQUEST))

        # Check if group exists
        group_obj = get_object_or_404(Group.objects.all(), pk=group_pk)
    else:
        group_obj = None

    # Serialize user
    serializer = UserSerializer(data=user_data, many=False, partial=True)

    # Save model in db if it is valid
    if serializer.is_valid():
        
        user = User(
            group=group_obj,
            email=user_data['email'],
            date_joined=user_data['date_joined'],
            last_login=user_data['last_login'],
            is_staff=user_data['is_staff'],
            first_name=user_data['first_name'],
            last_name=user_data['last_name']
        )

        # Set user password and save
        if password:
            user.set_password(password)

        user.save()

        return(Response({
            'detail': 'User created.',
        }, status=status.HTTP_201_CREATED))

    # Serializer was not valid
    return(Response({
        'detail': 'Bad request.',
    }, status=status.HTTP_400_BAD_REQUEST))


def createGroup(request):
    data = request.data
    name = data.get('name', False)
    description = data.get('description', "")
    color = data.get('color', "#FFFFFF")

    if not name:
        return(Response({
            'detail': 'Must have name.',
        }, status=status.HTTP_400_BAD_REQUEST))
    
    group = Group(
        name=name,
        description=description,
        color=color,
    )

    group.save()

    serializer = GroupSerializer(group, many=False)
    return(Response(serializer.data, status=status.HTTP_201_CREATED))


# Create election from post request TODO change request.data to request.POST
def createElection(request):
    data = request.data
    questions = data.get('questions', False)
    title = data.get('title', False)
    description = data.get('description', False)
    voting_starts_at = data.get('voting_starts_at', False)
    voting_ends_at = data.get('voting_ends_at', False)
    number_of_polls = int(data.get('number_of_polls', 0))
    owner_id = data.get('owner', False)
    groups_ids = data.get('groups', False)
    manual_closing = data.get('manual_closing', None);

    # Validate if basic data is provided
    if not questions or not title or not voting_ends_at or not voting_starts_at or not groups_ids or not owner_id:
        return(Response({
            'detail': 'Missing data.',
        }, status=status.HTTP_400_BAD_REQUEST))

    # Complete number of polls
    if not number_of_polls:
        number_of_polls = len(questions)

    # Check if manual closing was passed
    if manual_closing is None:
        return(Response({
            'detail': 'Missing data.',
        }, status=status.HTTP_400_BAD_REQUEST))

    # Get owner
    owner = get_object_or_404(User.objects.all(), pk=owner_id)

    # Get groups, if lengths of lists are not the same raise bad request
    groups = Group.objects.filter(id__in=groups_ids).distinct()

    if len(groups) != len(groups_ids):
        return(Response({
            'detail': 'Not all groups exists.',
        }, status=status.HTTP_400_BAD_REQUEST))

    # Create election object
    election = Election.objects.create(
        title=title,
        description=description,
        owner=owner,
        manual_closing=manual_closing,
        voting_starts_at=datetime.strptime(voting_starts_at, "%Y-%m-%dT%H:%M:%S%z"),
        voting_ends_at=datetime.strptime(voting_ends_at, "%Y-%m-%dT%H:%M:%S%z"),
        number_of_polls=number_of_polls,
    )

    # Add voting groups
    for group in groups:
        election.groups.add(group)

    # Lists to hold all created questions and options, in case of invalidity, delete all created objects
    q_list = []
    o_list = []

    # Iterate each question and create it
    for q in questions:
        question_options = q.get('options', None)
        question_title = q.get('title', False)
        question_desc = q.get('description', '')
        question_select = q.get('selection_type', False)
        question_min_select = q.get('min_selections', 1)
        question_max_select = q.get('max_selections', 1 if not question_options else len(question_options))
        question_order = q.get('order', 0)

        # If a question is not valid, delete all constructed data and return response
        if not question_title or not question_select or not question_options:
            election.delete()

            for del_q in q_list:
                del_q.delete()
            
            for del_o in o_list:
                del_o.delete()

            return(Response({
                'detail': 'Invalid question.',
            }, status=status.HTTP_400_BAD_REQUEST))

        # Create question
        question = Question.objects.create(
            title=question_title,
            description=question_desc,
            selection_type=question_select,
            min_selections=question_min_select,
            max_selections=question_max_select,
            order=question_order,
            election=election
        )

        # Append question to question list
        q_list.append(question)

        # for option in question.options
        for o in q['options']:
            option_value = o.get('value', False)
            option_order = o.get('order', 0)
            
            # Delete all data created so far if option not valid
            if not option_value:
                election.delete()

                for del_q in q_list:
                    del_q.delete()

                for del_o in o_list:
                    del_o.delete()

                return(Response({
                    'detail': 'Invalid option.',
                }, status=status.HTTP_400_BAD_REQUEST))

            option = Option.objects.create(
                value=option_value,
                order=option_order,
                question=question
            )

            o_list.append(option)
    
    serializer = SingleElectionSerializer(election ,many=False)
    
    return(Response(serializer.data, status=status.HTTP_201_CREATED))
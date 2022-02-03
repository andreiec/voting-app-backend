from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from src.models import User, Group
from src.serializers import UserSerializer, GroupSerializer


import uuid


# Create user from post request
def createUser(request):

    # Get data from post request
    data = request.POST
    email = data.get('email', False)
    password = data.get('password', False)
    group = data.get('group', False)
    is_staff = data.get('is_staff', False)

    # Check if data contains email and password
    if not email or not password:
        return(Response({
            'detail': 'Missing data from sender.',
        }, status=status.HTTP_400_BAD_REQUEST))

    # Check if mail already exists in db
    if User.objects.filter(email=email).exists():
        return(Response({
            'detail': 'Mail already exists.',
        }, status=status.HTTP_400_BAD_REQUEST))

    # Create unique id for user
    id = uuid.uuid4()

    # Create user dict with data for serialization
    user_data = {
        'email': email,
        'first_name': data.get('first_name', ""),
        'last_name': data.get('last_name', ""),
        'id': id,
        'date_joined': str(timezone.now()),
        'last_login': str(timezone.now()),
        'is_staff': is_staff == "True",
    }

    # If group is transmited through the body, check if it exists
    if group:

        # Check if id is a valid uuid
        try:
            group_pk = uuid.UUID(group, version=4)
        except:
            return(Response({
                'detail': 'Bad group id.',
            }, status=status.HTTP_400_BAD_REQUEST))

        # Check if group exists
        group_obj = get_object_or_404(Group.objects.all(), pk=group_pk)


    # Serialize user
    serializer = UserSerializer(data=user_data, many=False, partial=True)

    # Save model in db if it is valid
    if serializer.is_valid():
        
        user = User(
            id=id,
            group=group_obj,
            email=user_data['email'],
            date_joined=user_data['date_joined'],
            last_login=user_data['last_login'],
            is_staff=user_data['is_staff'],
            first_name=user_data['first_name'],
            last_name=user_data['last_name']
        )

        # Set user password and save
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
    data = request.POST
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
    return(Response(serializer.data))
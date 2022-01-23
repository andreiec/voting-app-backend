from rest_framework import status
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from src.models import User, Group
from src.serializers import UserSerializer, GroupSerializer


from bson import ObjectId


# Create user from post request
def createUser(request):

    data = request.POST
    email = data.get('email', False)
    password = data.get('password', False)
    group = data.get('group', False)

    # Check if data contains email and password
    if not email and not password:
        return(Response({
            'detail': 'Missing data from sender.',
        }, status=status.HTTP_400_BAD_REQUEST))

    # Check if mail already exists in db
    if User.objects.filter(email=email).exists():
        return(Response({
            'detail': 'Mail already exists.',
        }, status=status.HTTP_400_BAD_REQUEST))

    # Create user model with data
    user = User(
        email=email,
        first_name=data.get('first_name', ""),
        last_name=data.get('last_name', ""),
    )

    # Check if user is_staff
    if data.get('is_staff', False):
        if data.get('is_staff') == "True":
            user.is_staff = True
        else:
            user.is_staff = False

    # Set group if exists.
    if group:
        group_obj = get_object_or_404(Group.objects.all(), pk=ObjectId(group))
        user.group = group_obj

    # Set password
    user.set_password(password)
    
    # Save model in db
    user.save()

    serializer = UserSerializer(user, many=False)
    return(Response(serializer.data))


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
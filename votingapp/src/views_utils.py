from rest_framework import status
from rest_framework.response import Response

from src.models import User, Group
from src.serializers import UserSerializer

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
            'status' : 'Bad request',
            'message': 'Missing data from sender.',
        }, status=status.HTTP_400_BAD_REQUEST))

    # Check if mail already exists in db
    if User.objects.filter(email=email).exists():
        return(Response({
            'status' : 'Bad request',
            'message': 'Mail already exists.',
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

    # Set group if exists. If exists and is not valid, return error
    if group:
        try:
            group_obj = Group.objects.get(_id=ObjectId(data.get('group')))
            user.group = group_obj
        except:
            return(Response({
                'status' : 'Bad request',
                'message': 'Group does not exist.',
            }, status=status.HTTP_400_BAD_REQUEST))

    # Set password
    user.set_password(password)
    
    # Save model in db
    user.save()

    serializer = UserSerializer(user, many=False)
    return(Response(serializer.data))
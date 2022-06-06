from dataclasses import field
from rest_framework import serializers
from .models import ClosedElection, Option, Question, Submission, User, Group, Election, Vote

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    group = GroupSerializer(many=False, read_only=True)
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'group', 'date_joined', 'last_login', 'is_staff', 'is_active']


# Serializer for option when inside an election JSON
class ElectionOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        exclude = ['question']


# Serializer for question when inside an election JSON
class ElectionQuestionSerializer(serializers.ModelSerializer):
    options = serializers.SerializerMethodField()

    class Meta:
        model = Question
        exclude = ['election']


    def get_options(self, object):
        options = object.option_set.all()
        serializer = ElectionOptionSerializer(options, many=True)
        return serializer.data


# Serializer for multiple elections
class SingleElectionSerializer(serializers.ModelSerializer):
    questions = serializers.SerializerMethodField()

    class Meta:
        model = Election
        fields = "__all__"

    def get_questions(self, object):
        questions = object.question_set.all()
        serializer = ElectionQuestionSerializer(questions, many=True)
        return serializer.data


# Serializer for a single election
class MultipleElectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Election
        fields = "__all__"


class ClosedElectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClosedElection
        fields = "__all__"


# Base serializer for submission
class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ['user']


# Base serializer for vote
class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ['option']
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.hashers import make_password
from django.db.models.deletion import CASCADE, SET, SET_NULL
from django.core.validators import MaxValueValidator

from colorfield.fields import ColorField
from utils import CustomUserManager

import uuid


# Base group class
class Group(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    
    name = models.CharField(max_length=128, null=True, blank=False, unique=True)
    description = models.TextField(max_length=2048, null=True, blank=True)
    color = ColorField(default="#dddddd")


    def __str__(self):
        return self.name


# Custom user model
class User(AbstractBaseUser):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    email = models.EmailField(verbose_name='email', max_length=120, unique=True)

    username = None

    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    # Extra fields for User
    profile_picture = models.ImageField(max_length=255, upload_to='profile_pictures/', null=True, blank=True, default='profile_pictures/default-user.png')
    first_name = models.CharField(max_length=60, null=True, blank=True)
    last_name = models.CharField(max_length=60, null=True, blank=True)
    group = models.ForeignKey(Group, on_delete=SET_NULL, null=True, blank=True)


    def __str__(self):
        return self.email


    def has_perm(self, perm, obj=None):
        return self.is_admin

    
    def has_module_perms(self, app_label):
        return True


    def validate_password(self, value):
        return make_password(value)



# Class for election
class Election(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)

    owner = models.ForeignKey(User, on_delete=SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=False)
    description = models.TextField(max_length=4000, null=True, blank=True)

    voting_starts_at = models.DateTimeField(auto_now_add=False, default=None, null=True, blank=True)
    voting_ends_at = models.DateTimeField(auto_now_add=False, default=None, null=True, blank=True)
    archived_at = models.DateTimeField(auto_now_add=False, default=None, null=True, blank=True)

    accepts_votes = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_archived = models.BooleanField(default=False)

    number_of_polls = models.PositiveSmallIntegerField(blank=False, null=False, validators=[MaxValueValidator(100)])
    groups = models.ManyToManyField('Group', blank=True)


    def __str__(self):
        return self.title


    class Meta:
        ordering = ['-created']


# Base class for question inside of Election TODO add minimum and maximum choices
class Question(models.Model):
    SELECTION_CHOICES = [
        ('single', 'Single Select'),
        ('multiple', 'Multiple Select')
    ]

    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    election = models.ForeignKey(Election, on_delete=models.CASCADE, null=True, blank=True)

    title = models.CharField(max_length=255, null=True, blank=False)
    description = models.TextField(max_length=4000, null=True, blank=True)
    selection_type = models.CharField(max_length=15, choices=SELECTION_CHOICES, default='single_select')
    min_selections = models.PositiveIntegerField(null=True, blank=True)
    max_selections = models.PositiveIntegerField(null=True, blank=True)
    order = models.PositiveSmallIntegerField(blank=False, null=False, default=0, validators=[MaxValueValidator(100)])

    def __str__(self):
        return self.title


    class Meta:
        ordering = ['order']


# Base class for Option
class Option(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True, blank=True)

    value = models.CharField(max_length=255, null=True, blank=False)
    order = models.PositiveSmallIntegerField(blank=False, null=False, default=0, validators=[MaxValueValidator(100)])

    def __str__(self):
        return self.value


    class Meta:
        ordering = ['order']


# Base class for a vote
class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=False, blank=False)
    option = models.ForeignKey(Option, on_delete=models.DO_NOTHING, null=False, blank=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [['user', 'option']]


    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}: {self.option.value}'


# Base class for a submission (Used to hold information if an user voted on an election)
class Submission(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=False, blank=False)
    election = models.ForeignKey(Election, on_delete=models.DO_NOTHING, null=False, blank=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [['user', 'election']]


    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}: {self.election.title}'
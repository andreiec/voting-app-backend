from djongo import models
from django.contrib.auth.models import User
from colorfield.fields import ColorField
from django.db.models.deletion import CASCADE, SET, SET_NULL


# Base group class
class Group(models.Model):
    _id = models.ObjectIdField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    
    name = models.CharField(max_length=128, null=True, blank=False, unique=True)
    description = models.TextField(max_length=2048, null=True, blank=True)
    color = ColorField(default="#dddddd")


    def __str__(self):
        return self.name


# Base profile class
class Profile(models.Model):
    _id = models.ObjectIdField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)

    user = models.OneToOneField(User, db_column='user', on_delete=models.CASCADE, null=True, blank=True)
    group = models.ForeignKey(Group, db_column='group', to_field='_id', on_delete=SET_NULL, null=True, blank=True)

    email = models.EmailField(max_length=100, blank=True, null=True)
    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)

    is_staff = models.BooleanField(default=False, null=False, blank=False)
    is_active = models.BooleanField(default=True, null=False, blank=False)


    def __str__(self):
        return f"{self.last_name} {self.first_name}"
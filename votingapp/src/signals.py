import email
import profile
from .models import Profile
from django.db.models.signals import post_delete, post_save
from django.contrib.auth.models import User


# Create a profile when user is created
def createProfile(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name
        )


# When a profile is updated, update the user model
def updateUser(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user
    if created == False:
        user.first_name = profile.fist_name
        user.last_name = profile.last_name
        user.email = profile.email
        user.save()


# When profile is deleted make sure user is deleted too
def deleteUser(sender, instance, **kwargs):
    user = instance.user
    user.delete()


post_save.connect(createProfile, sender=User)
post_save.connect(updateUser, sender=Profile)
post_delete.connect(deleteUser, sender=Profile)
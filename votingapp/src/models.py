from djongo import models
from django.contrib.auth.models import User


# Base profile class
class Profile(models.Model):
    _id = models.ObjectIdField()
    created = models.DateTimeField(auto_now_add=True)

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)


    def __str__(self):
        return f"{self.last_name} {self.first_name}"
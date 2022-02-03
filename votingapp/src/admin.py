from django.contrib import admin
from .models import User, Group, Election, Question, Option, Vote

# Register your models here.
admin.site.register(User)
admin.site.register(Group)
admin.site.register(Election)
admin.site.register(Question)
admin.site.register(Option)
admin.site.register(Vote)
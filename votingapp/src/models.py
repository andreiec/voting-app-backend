from djongo import models
from django.contrib.auth.models import AbstractBaseUser
from colorfield.fields import ColorField
from django.db.models.deletion import CASCADE, SET, SET_NULL
from utils import CustomUserManager


# Base group class
class Group(models.Model):
    _id = models.ObjectIdField()
    created = models.DateTimeField(auto_now_add=True)
    
    name = models.CharField(max_length=128, null=True, blank=False, unique=True)
    description = models.TextField(max_length=2048, null=True, blank=True)
    color = ColorField(default="#dddddd")


    def __str__(self):
        return self.name


# Custom user model
class User(AbstractBaseUser):
    
    # Base fields of Abstract User
    _id = models.ObjectIdField()
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
    group = models.ForeignKey(Group, db_column='group', to_field='_id', on_delete=SET_NULL, null=True, blank=True)


    def __str__(self):
        return self.email


    def has_perm(self, perm, obj=None):
        return self.is_admin

    
    def has_module_perms(self, app_label):
        return True


    # Return the string value of group id
    def get_group_id(self):
        if self.group is not None:
            return str(self.group._id)
        return None


    # Return the string value of id
    def get_id(self):
        return str(self._id)

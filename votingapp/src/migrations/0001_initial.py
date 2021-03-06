# Generated by Django 4.0.1 on 2022-02-03 15:25

import colorfield.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import utils
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('email', models.EmailField(max_length=120, unique=True, verbose_name='email')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='date joined')),
                ('last_login', models.DateTimeField(auto_now=True, verbose_name='last login')),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('profile_picture', models.ImageField(blank=True, default='profile_pictures/default-user.png', max_length=255, null=True, upload_to='profile_pictures/')),
                ('first_name', models.CharField(blank=True, max_length=60, null=True)),
                ('last_name', models.CharField(blank=True, max_length=60, null=True)),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', utils.CustomUserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=128, null=True, unique=True)),
                ('description', models.TextField(blank=True, max_length=2048, null=True)),
                ('color', colorfield.fields.ColorField(default='#dddddd', image_field=None, max_length=18, samples=None)),
            ],
        ),
        migrations.CreateModel(
            name='Election',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(max_length=255, null=True)),
                ('description', models.TextField(blank=True, max_length=4000, null=True)),
                ('voting_starts_at', models.DateTimeField(default=None, null=True)),
                ('voting_ends_at', models.DateTimeField(default=None, null=True)),
                ('archived_at', models.DateTimeField(default=None, null=True)),
                ('accepts_votes', models.BooleanField(default=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_archived', models.BooleanField(default=False)),
                ('number_of_polls', models.IntegerField()),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='src.group'),
        ),
    ]

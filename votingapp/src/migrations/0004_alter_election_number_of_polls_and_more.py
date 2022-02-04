# Generated by Django 4.0.1 on 2022-02-04 14:56

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('src', '0003_alter_election_archived_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='election',
            name='number_of_polls',
            field=models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(100)]),
        ),
        migrations.AlterField(
            model_name='question',
            name='selection_type',
            field=models.CharField(choices=[('Single', 'single_select'), ('Multiple', 'multiple_select')], default='single_select', max_length=15),
        ),
    ]

# Generated by Django 3.0.3 on 2020-04-01 11:49

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('poster', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='conference',
            name='attendees_group',
        ),
        migrations.RemoveField(
            model_name='conference',
            name='guests_group',
        ),
        migrations.RemoveField(
            model_name='conference',
            name='organizers_group',
        ),
        migrations.AlterField(
            model_name='conference',
            name='attendees',
            field=models.ManyToManyField(related_name='attendees', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='conference',
            name='guests',
            field=models.ManyToManyField(related_name='guests', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='conference',
            name='organizers',
            field=models.ManyToManyField(related_name='organizers', to=settings.AUTH_USER_MODEL),
        ),
    ]

from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from core.models import User


class Conference(models.Model):
    title = models.CharField(max_length=50)
    institution = models.CharField(max_length=50)
    description = models.TextField()
    attendees = models.ManyToManyField(User)
    created_date = models.DateTimeField('created date', auto_now=True)
    is_private = False

    def __str__(self):
        return self.title


class Poster(models.Model):
    image = models.ImageField(blank=True, null=True)
    title = models.CharField(max_length=50)
    subtitle = models.CharField(max_length=50)
    authors = models.ManyToManyField(User)
    description = models.TextField()
    created_date = models.DateTimeField('created date')
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Comment(models.Model):
    poster = models.ForeignKey(Poster, on_delete=models.CASCADE)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    body = models.TextField()
    created_date = models.DateTimeField('created date', auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created_date']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)


# class Organizers(Group):


# class Attendees():
#     ...


# class Guests():
#     ...

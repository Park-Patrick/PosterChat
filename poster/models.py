from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from core.models import User
from typing import List


class Conference(models.Model):
    title = models.CharField(max_length=50)
    institution = models.CharField(max_length=50)
    description = models.TextField()

    organizers = models.ManyToManyField(
        get_user_model(), related_name="organizers")
    attendees = models.ManyToManyField(
        get_user_model(), related_name="attendees")
    guests = models.ManyToManyField(get_user_model(), related_name="guests")

    created_date = models.DateTimeField('created date', auto_now=True)
    is_public = models.BooleanField(
        "is conference publically accessible", default=True)

    def update_organizers(self):
        if self.organizers != self._original_organizers:
            self.update_group(new_organizers, "organizers")
            self._original_organizers = self.organizers

        if self.attendees != self._original_attendees:
            self.update_group(new_attendees, "attendees")
            self._original_attendees = self.attendees

        if self.guests != self._original_guests:
            self.update_group(new_guests, "guests")
            self._original_guests = self.guests

    def update_group(self, new_users: List[User], group_name: str):
        current_users = getattr(self, group_name)

        group = getattr(self, group_name + "_group")

        to_rem = [o for o in current_users if o not in new_users]
        to_add = [o for o in new_users if o not in current_users]

        for o in to_rem:
            group.user_set.remove(o)

        for o in to_add:
            group.user_set.add(o)

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

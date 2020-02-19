from django.db import models
from django.utils import timezone

# Create your models here.

# create model of a typical post
class Post(models,Model):
	author = models.ForeignKey('auth.User',on_delete=models.CASCADE)
	image = models.ImageField(blank=True, null=True)
	caption = models.Textfield()
	created_date = models.DateTimeField(default=timezone.now)
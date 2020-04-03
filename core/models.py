from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as trans
from PIL import Image


class UserManager(BaseUserManager):
    """Implements Django user manager to use the custom user in PosterChat

    Django expects UserManager interface as such:
    https://docs.djangoproject.com/en/3.0/topics/auth/customizing/#writing-a-manager-for-a-custom-user-model
    """

    def create_user(self, email, first_name, last_name, username, password=None, commit=True):

        if not email:
            raise ValueError(trans("Users must have an email address"))

        if not first_name:
            raise ValueError(trans('Users must have a first name'))

        if not last_name:
            raise ValueError(trans("Users must have a last name"))

        if not username:
            raise ValueError(trans("Users must have a username"))

        user = self.model(email=self.normalize_email(email),
                          first_name=first_name, last_name=last_name, username=username)

        user.set_password(password)
        if commit:
            user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, username, password):
        user = self.create_user(
            email, password=password, first_name=first_name, last_name=last_name, username=username, commit=False)

        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Implements Django user for use in PosterChat

    Django expects User models to support the following interface
    https://docs.djangoproject.com/en/3.0/topics/auth/customizing/#specifying-a-custom-user-model
    """

    email = models.EmailField(verbose_name=trans(
        "email address"), max_length=255, unique=True)

    # No need for password and last_login since this is provided via super
    first_name = models.CharField(
        trans("first name"), max_length=30, blank=True)
    last_name = models.CharField(
        trans("last name"), max_length=150, blank=True)

    username = models.SlugField(trans("user name"), max_length=30, unique=True)

    is_active = models.BooleanField(trans('active'), default=True, help_text=trans(
        "Use this to delete accounts. Inactive (False) accounts should be treated as if they're deleted."))

    is_staff = models.BooleanField(trans("staff status"), default=False, help_text=trans(
        "If True, user can log into the admin site."))

    date_joined = models.DateTimeField(
        trans("date joined"), default=timezone.now)
    objects = UserManager()

    avatar = models.ImageField(
        "Profile Image", default="default-avatar.png", upload_to="avatar_images")

    description = models.TextField("Bio", default="")

    # Conferences attended, Posters authored, Comments,

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["first_name", "last_name", "username"]

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def get_short_name(self):
        return self.first_name.strip()

    def __str__(self):
        return f"{self.get_full_name()} <{self.email}>"

    def save(self, *args, **kwargs):
        img = Image.open(self.avatar.path)

        if img.height > 200 or img.width > 200:
            img.thumbnail((200, 200))
            img.save(self.avatar.path)

        super().save()

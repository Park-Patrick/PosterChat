from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as trans
from django.core.exceptions import ValidationError
from PIL import Image
import re


def validate_name(name: str):
    if name.startswith('-') or name.endswith('-'):
        msg = "%(name)s cannot start or end with '-'."
    elif name.startswith(' ') or name.endswith(' '):
        msg = "%(name)s cannot start or end with spaces."
    elif not re.match(r'^[A-Za-z-\s]+$', name):
        msg = "%(name)s can only have letters, and hyphen."
    elif re.match(r'.*[-]{2,}.*', name):
        msg = "%(name)s cannot have multiple '-' in a row."
    elif re.match(r'.*[\s]{2,}.*', name):
        msg = "%(name)s cannot have multiple spaces in a row."
    else:
        return
    raise ValidationError(trans(msg), "invalid_name", {"name": name})


def validate_username(name: str):
    if not re.match(r'^[A-Za-z\d_]+$', name):
        msg = "%(name)s can only have letters, numbers and underscore."
    elif len("".join(letter for letter in name if letter.isalnum())) < 5:
        msg = "%(name)s must be at least 5 alphanumeric chars long."
    elif name[0].isdigit():
        msg = "%(name)s cannot start with a number.",
    elif name.startswith('_') or name.endswith('_'):
        msg = "%(name)s cannot start or end with underscore."
    elif re.match(r'.*[_]{2,}.*', name):
        msg = "%(name)s cannot have multiple '_' in a row."
    else:
        return

    raise ValidationError(trans(msg), "invalid_username", {"name": name})


class UserManager(BaseUserManager):
    """Implements Django user manager to use the custom user in PosterChat

    Django expects UserManager interface as such:
    https://docs.djangoproject.com/en/3.0/topics/auth/customizing/#writing-a-manager-for-a-custom-user-model
    """

    def create_user(self, email, first_name, last_name, username, password=None, commit=True, **extra_kwargs):

        if not email:
            raise ValueError(trans("Users must have an email address"))

        if not first_name:
            raise ValueError(trans('Users must have a first name'))

        if not last_name:
            raise ValueError(trans("Users must have a last name"))

        if not username:
            raise ValueError(trans("Users must have a username"))

        user = self.model(email=self.normalize_email(email), first_name=first_name,
                          last_name=last_name, username=username, **extra_kwargs)

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

    first_name = models.CharField(
        trans("first name"), max_length=30, blank=True, validators=[validate_name])
    last_name = models.CharField(
        trans("last name"), max_length=150, blank=True, validators=[validate_name])

    # 16 chars max
    # 5 chars min
    # Alphanumeric with -,_
    # Must have at least 1 letter
    # Not allowed to start with number
    # Cannot include multiple in class [-,_] in a row
    # No trailing/prefixing [-,_]

    username = models.SlugField(
        trans("user name"), max_length=16, unique=True, validators=[validate_username])

    is_active = models.BooleanField(trans('active'), default=True, help_text=trans(
        "Use this to delete accounts. Inactive (False) accounts should be treated as if they're deleted."))

    is_staff = models.BooleanField(trans("staff status"), default=False, help_text=trans(
        "If True, user can log into the admin site."))

    date_joined = models.DateTimeField(
        trans("date joined"), default=timezone.now)
    objects = UserManager()

    avatar = models.ImageField(
        "Profile Image", blank=True, upload_to="avatar_images")

    description = models.TextField("Bio", blank=True)

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
        super().save(*args, **kwargs)
        if self.avatar:
            img = Image.open(self.avatar.path)

            if img.height > 200 or img.width > 200:
                img.thumbnail((200, 200))
                img.save(self.avatar.path)
                super().save()

    def clean(self):
        super().clean()

        # Clean first and last name
        validate_name(self.first_name)
        validate_name(self.last_name)
        validate_username(self.username)

        # setattr(self, self.USERNAME_FIELD, self.normalize_username(self.get_username()))

        # Clean username

        # Clean email

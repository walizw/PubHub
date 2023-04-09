from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.conf import settings

from .Profile import Profile

from ..crypto import keypair_gen


class ActivityUserManager(BaseUserManager):
    """Custom user model manager used to create an ActivityUser model."""

    def create_user(self, username, email, password=None):
        """Create and return a `User` with an email, username, password and its keypair."""
        if username is None:
            raise TypeError("Users should have a username")
        if email is None:
            raise TypeError("Users should have an email")

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)

        # Generate the keypair
        user.priv_key, user.pub_key = keypair_gen.generate_keypair()
        user.save()

        # create a profile
        profile = Profile.objects.create(
            id=f"https://{settings.AP_DOMAIN}/api/v1/users/{user.username}",
            preferred_username=user.username,
            inbox=f"https://{settings.AP_DOMAIN}/api/v1/users/{user.username}/inbox",
            outbox=f"https://{settings.AP_DOMAIN}/api/v1/users/{user.username}/outbox",
            followers=f"https://{settings.AP_DOMAIN}/api/v1/users/{user.username}/followers",
            following=f"https://{settings.AP_DOMAIN}/api/v1/users/{user.username}/following",
            public_key=user.pub_key,
            shared_inbox=f"https://{settings.AP_DOMAIN}/api/v1/inbox",
        )
        profile.save()

        return user

    def create_superuser(self, username, email, password=None):
        """Create and return a `User` with superuser powers."""
        if password is None:
            raise TypeError("Password should not be none")

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class ActivityUser (AbstractBaseUser):
    """Custom user model with the fields required to the activitypub implementation"""

    # Default user fields
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    # Social fields
    followers = models.IntegerField(default=0)
    following = models.IntegerField(default=0)

    # ActivityPub fields
    name = models.CharField(max_length=255, blank=True)
    summary = models.TextField(blank=True)

    pub_key = models.TextField(blank=False)
    priv_key = models.TextField(blank=False)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    objects = ActivityUserManager()

    def __str__(self):
        return self.username

    def get_full_name(self):
        """Used to get a user's full name."""
        return self.username

    def get_short_name(self):
        """Used to get a user's short name."""
        return self.username

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        return self.is_superuser

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        return self.is_superuser

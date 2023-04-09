from django.db import models


class Profile (models.Model):
    # all users have a profile (even external users)
    id = models.CharField(max_length=255, primary_key=True)
    preferred_username = models.CharField(max_length=255)

    inbox = models.CharField(max_length=255)
    outbox = models.CharField(max_length=255)
    followers = models.CharField(max_length=255)
    following = models.CharField(max_length=255)

    public_key = models.TextField()
    shared_inbox = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.preferred_username}"

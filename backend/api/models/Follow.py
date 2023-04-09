from django.db import models

from .Profile import Profile


class Follow (models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    actor = models.ForeignKey(
        Profile, on_delete=models.CASCADE)  # who is following
    object = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="followed_profile")  # who is being followed
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.actor} follows {self.object}"

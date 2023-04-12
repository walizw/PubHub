from django.db import models

from .Profile import Profile
from .Note import Note


class Like (models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    actor = models.ForeignKey(
        Profile, on_delete=models.CASCADE)  # who is following
    object = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="liked_note")  # who is being followed
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.actor.preferred_username} liked {self.object.preferred_username}'s post"

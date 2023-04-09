from django.db import models

from .Profile import Profile


class Note (models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    actor = models.ForeignKey(Profile, on_delete=models.CASCADE)

    content = models.TextField()
    published = models.DateTimeField()
    tags = models.TextField(null=True, blank=True)

    # TODO: Handle attachments and mentions

    def __str__(self):
        return f"{self.actor.preferred_username} published \"{self.content}\""

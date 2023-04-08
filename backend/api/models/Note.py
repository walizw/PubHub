from django.db import models


class Note (models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    actor = models.CharField(max_length=255)

    content = models.TextField()
    published = models.DateTimeField()
    tags = models.TextField()

    # TODO: Handle attachments and mentions

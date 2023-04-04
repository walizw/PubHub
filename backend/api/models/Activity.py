from django.db import models


class Activity(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    type = models.CharField(max_length=255)
    actor = models.CharField(max_length=255)

    # this is text, in case there are several, they will be splitten by a comma
    to = models.TextField(null=True)
    cc = models.TextField(null=True)

    # TODO: There should be a better way to store dictionaries (if needed)
    object = models.TextField(null=True)

    content = models.TextField(null=True)
    source = models.TextField(null=True)

    published = models.DateTimeField(null=True)
    deleted = models.DateTimeField(null=True)

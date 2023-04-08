from django.db import models


class DiscoveredInstances(models.Model):
    url = models.CharField(max_length=255, unique=True)

    inbox = models.CharField(max_length=255, null=True)

from django.db import models


class DiscoveredInstances(models.Model):
    class Meta:
        verbose_name = "Discovered Instance"
        verbose_name_plural = "Discovered Instances"
    url = models.CharField(max_length=255, unique=True)

    inbox = models.CharField(max_length=255, null=True)

    def __str__(self):
        return f"{self.url}"

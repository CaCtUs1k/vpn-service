from django.contrib.auth.models import User
from django.db import models


class Site(models.Model):
    user = models.ForeignKey(User, related_name="sites", on_delete=models.CASCADE)
    name = models.CharField(max_length=63, unique=True)
    url = models.URLField()


class Statistic(models.Model):
    user = models.ForeignKey(User, related_name="connections", on_delete=models.CASCADE)
    site = models.ForeignKey(Site, related_name="connections", on_delete=models.CASCADE)
    page_views = models.PositiveIntegerField(default=0)
    data_sent = models.PositiveIntegerField(default=0)
    data_received = models.PositiveIntegerField(default=0)

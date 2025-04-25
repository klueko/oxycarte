# models.py
from django.db import models

class PollutionData(models.Model):
    city = models.CharField(max_length=100)
    aqi = models.IntegerField(null=True, blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

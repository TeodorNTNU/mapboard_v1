from django.db import models
from django.utils import timezone


class ElectricityData(models.Model):
    city = models.CharField(max_length=255, db_index=True)
    state = models.CharField(max_length=255, db_index=True)
    date = models.DateField(db_index=True)
    region = models.CharField(max_length=255, db_index=True)
    NOK_per_kWh = models.FloatField()
    EUR_per_kWh = models.FloatField()
    EXR = models.FloatField()
    time_start = models.CharField(max_length=255)
    time_end = models.CharField(max_length=255)
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'electricity_prices'
        unique_together = (('region', 'date', 'time_start'),)
        indexes = [
            models.Index(fields=['city']),
            models.Index(fields=['state']),
            models.Index(fields=['date']),
            models.Index(fields=['region']),
        ]
        

class WeatherData(models.Model):
    city = models.CharField(max_length=255, db_index=True)
    state = models.CharField(max_length=255, db_index=True)
    date = models.DateField(db_index=True)
    temperature = models.FloatField()
    time_start = models.CharField(max_length=255)
    time_end = models.CharField(max_length=255)
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'weather_data'
        unique_together = (('city', 'date', 'time_start'),)
        indexes = [
            models.Index(fields=['city']),
            models.Index(fields=['state']),
            models.Index(fields=['date']),
        ]

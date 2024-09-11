from django.contrib.gis.db import models

class Region(models.Model):
    name = models.CharField(max_length=255)
    geom = models.MultiPolygonField()  # PostGIS field for geographic data

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'geospatial'  # Ensures that this app uses the geospatial database

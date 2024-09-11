from django.core.management.base import BaseCommand
from geospatial.models import Region
from django.contrib.gis.geos import GEOSGeometry, Polygon, MultiPolygon
import json

class Command(BaseCommand):
    help = "Import GeoJSON data, converting all geometries to MultiPolygon if needed"

    def handle(self, *args, **kwargs):
        # Path to the new GeoJSON file
        geojson_file = '/home/teodorrk/projects/sql_chatbot/frontend/public/aligned_non_overlapping_map.geojson'
        
        # Load the GeoJSON file
        with open(geojson_file, 'r') as f:
            geojson_data = json.load(f)

        for feature in geojson_data['features']:
            name = feature['properties'].get('name', 'Unnamed region')

            # Load the geometry
            geometry = GEOSGeometry(json.dumps(feature['geometry']))

            # Ensure that all geometries are converted to MultiPolygon
            if isinstance(geometry, Polygon):
                geometry = MultiPolygon(geometry)  # Convert Polygon to MultiPolygon
            elif not isinstance(geometry, MultiPolygon):
                self.stdout.write(self.style.ERROR(f"Unsupported geometry type for feature: {name}"))
                continue

            # Save the region to the database
            region, created = Region.objects.get_or_create(
                name=name,
                defaults={'geom': geometry}
            )

            if not created:
                region.geom = geometry
                region.save()

        self.stdout.write(self.style.SUCCESS('Successfully imported GeoJSON data.'))

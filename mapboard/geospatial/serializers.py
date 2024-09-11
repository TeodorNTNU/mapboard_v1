from rest_framework_gis.serializers import GeoFeatureModelSerializer
from geospatial.models import Region

class RegionGeoSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Region
        geo_field = "geom"
        fields = ['id', 'name']

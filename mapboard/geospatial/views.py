from rest_framework import viewsets
from geospatial.models import Region
from geospatial.serializers import RegionGeoSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication


class RegionGeoViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A viewset for viewing GeoJSON of Regions. Read-only operations allowed.
    """
    queryset = Region.objects.all()
    serializer_class = RegionGeoSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        print(serializer.data)  # Debug: Print serialized data to verify
        return Response(serializer.data)
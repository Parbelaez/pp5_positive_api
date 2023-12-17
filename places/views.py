import logging

from rest_framework import filters, generics, permissions

from positive_api.permissions import IsOwnerOrReadOnly, CustomJWTCookieAuthentication

from .models import Place
from .serializers import PlaceSerializer

logger = logging.getLogger(__name__)


class PlaceList(generics.ListCreateAPIView):
    authentication_classes = [CustomJWTCookieAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = PlaceSerializer
    queryset = Place.objects.all().order_by("-created_at")

    # We add the filter and ordering backends to be able to filter and order
    # the places by name and city
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ["place_name", "city"]
    search_fields = ["place_name", "city"]

    def post(self, request, *args, **kwargs):
        try:
            logger.info("DEBERIA ESTAR EN EL POST DE CREATE LA PORONG AESTA")
            return super().post(request, *args, **kwargs)
        except Exception as e:
            logger.exception(f"Falla en el post {str(e)}")
            raise


class PlaceDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = PlaceSerializer
    queryset = Place.objects.all()

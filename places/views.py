from rest_framework import filters, generics, permissions
from rest_framework.exceptions import ValidationError

from positive_api.permissions import IsOwnerOrReadOnly

from .models import Place
from .serializers import PlaceSerializer


class PlaceList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = PlaceSerializer
    queryset = Place.objects.all().order_by("-created_at")

    # We add the filter and ordering backends to be able to filter and order
    # the places by name and city
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ["place_name", "city"]
    search_fields = ["place_name", "city"]


class PlaceDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = PlaceSerializer
    queryset = Place.objects.all()

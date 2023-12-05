from rest_framework import generics, permissions
from .models import Place
from .serializers import PlaceSerializer
from positive_api.permissions import IsOwnerOrReadOnly
from rest_framework.exceptions import ValidationError


class PlaceList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = PlaceSerializer
    queryset = Place.objects.all()

    def perform_create(self, serializer):
        place, created = Place.objects.get_or_create(
            place_name=self.request.data.get('place_name'), 
            city=self.request.data.get('city'), 
            defaults={'owner': self.request.user}
        )
        if not created:
            raise ValidationError(
                "A place with this name and city already exists."
                )
        serializer.save(owner=self.request.user)

class PlaceDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = PlaceSerializer
    queryset = Place.objects.all()
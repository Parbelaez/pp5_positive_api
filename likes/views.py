from rest_framework import generics, permissions
from .models import Likes
from .serializers import LikeSerializer
from positive_api.permissions import IsOwnerOrReadOnly


class LikeList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = LikeSerializer
    queryset = Likes.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class LikeDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = LikeSerializer
    queryset = Likes.objects.all()

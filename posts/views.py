from rest_framework import generics, permissions, filters
from .models import Post
from .serializers import PostSerializer
from positive_api.permissions import IsOwnerOrReadOnly
from django.db.models import Count


class PostList(generics.ListCreateAPIView):
    """
    List all posts, or create a new post when authenticated.
    The perform_create method is used to set the owner of the post to the
    current user.
    """
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Post.objects.annotate(
        num_top=Count('post_likes', filter=Count('post_likes', like_type='top')),
        num_like=Count('post_likes', filter=Count('post_likes', like_type='like')),
        num_dislike=Count('post_likes', filter=Count('post_likes', like_type='dislike'))
    ).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a post instance when authenticated and owner.
    """
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Post.objects.annotate(
        num_top=Count('post_likes', filter=Count('post_likes', like_type='top')),
        num_like=Count('post_likes', filter=Count('post_likes', like_type='like')),
        num_dislike=Count('post_likes', filter=Count('post_likes', like_type='dislike'))
    ).order_by('-created_at')
    serializer_class = PostSerializer


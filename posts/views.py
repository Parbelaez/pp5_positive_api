from rest_framework import generics, permissions, filters
from .models import Post
from .serializers import PostSerializer
from positive_api.permissions import IsOwnerOrReadOnly
from django.db.models import Count, Q


class PostList(generics.ListCreateAPIView):
    """
    List all posts, or create a new post when authenticated.
    The perform_create method is used to set the owner of the post to the
    current user.
    """
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Post.objects.annotate(
        # In previous versions of Django, we would have to use the
        #Case When statement. After Django 3.2, we can use the Count
        #function with the filter parameter to count the number of
        #likes of each type.
        num_top=Count('post_likes__like_type',
            filter=Q(post_likes__like_type='top')
            ),
        num_like=Count('post_likes__like_type',
            filter=Q(post_likes__like_type='like')
            ),
        num_dislike=Count('post_likes__like_type',
            filter=Q(post_likes__like_type='dislike')
            )
    ).order_by('-created_at')

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['post_place__place_name', 'post_place__city']
    ordering_fields = ['post_place__place_name',
        'post_place__city', 'created_at'
        ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a post instance when authenticated and owner.
    """
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Post.objects.annotate(
        num_top=Count('post_likes__like_type',
            filter=Q(post_likes__like_type='top')
            ),
        num_like=Count('post_likes__like_type',
            filter=Q(post_likes__like_type='like')
            ),
        num_dislike=Count('post_likes__like_type',
            filter=Q(post_likes__like_type='dislike')
            )
    ).order_by('-created_at')
    serializer_class = PostSerializer


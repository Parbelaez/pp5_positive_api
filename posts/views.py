from django.shortcuts import get_object_or_404
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Post
from .serializers import PostSerializer
from positive_api.permissions import IsOwnerOrReadOnly


class PostList(APIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    # We use get to retrieve all the posts
    def get(self, request):
        # get all the posts
        posts = Post.objects.all()
        # we need to serialize the data before sending it
        # and we set many to True because we are sending multiple objects
        # The context={'request': request} is needed to be able to have a
        # the request available in the serializer
        serializer = PostSerializer(
            posts, many=True, context={'request': request}
            )
        # return the serialized data (NOT THE OBJECTS!)
        return Response(serializer.data)

    # We use post to create a single post
    def post(self, request):
        # we serialize the data sent by the user
        serializer = PostSerializer(
            data=request.data, context={'request': request}
            )
        # if the serializer is valid, we save it
        if serializer.is_valid():
            serializer.save(owner=request.user)
            # and return the serialized data
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # if the serializer is not valid, return a 400 error
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostDetail(APIView):
    # We need to define the serializer class here to be able to have a proper
    # form in the browsable API
    serializer_class = PostSerializer
    # We need to define the permission class here to be able to have a proper
    # form in the browsable API depending on the user
    permission_classes = [IsOwnerOrReadOnly]
    # We use get_object to retrieve a single post
    def get_object(self, pk):
        post = get_object_or_404(Post, pk=pk)
        self.check_object_permissions(self.request, post)
        return post

    def get(self, request, pk):
        post = self.get_object(pk)
        serializer = PostSerializer(
            post, context={'request': request}
            )
        return Response(serializer.data)

    # We use put to update a single post
    def put(self, request, pk):
        post = self.get_object(pk)
        serializer = PostSerializer(
            post, data=request.data, context={'request': request}
            )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        # if the serializer is not valid, return a 400 error
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # We use delete to delete a single post
    def delete(self, request, pk):
        post = self.get_object(pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

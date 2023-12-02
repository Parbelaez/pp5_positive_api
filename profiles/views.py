from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Profile
from .serializers import ProfileSerializer
from positive_api.permissions import IsOwnerOrReadOnly

class ProfileList(APIView):
    # We use get to retrieve all the profiles
    def get(self, request):
        # get all the profiles
        profiles = Profile.objects.all()
        # we need to serialize the data before sending it
        # and we set many to True because we are sending multiple objects
        # The context={'request': request} is needed to be able to have a
        # the request available in the serializer
        serializer = ProfileSerializer(
            profiles, many=True, context={'request': request}
            )
        # return the serialized data (NOT THE OBJECTS!)
        return Response(serializer.data)

class ProfileDetail(APIView):
    # We need to define the serializer class here to be able to have a proper
    # form in the browsable API
    serializer_class = ProfileSerializer
    # We need to define the permission class here to be able to have a proper
    # form in the browsable API depending on the user
    permission_classes = [IsOwnerOrReadOnly]
    # We use get_object to retrieve a single profile
    def get_object(self, pk):
        profile = get_object_or_404(Profile, pk=pk)
        self.check_object_permissions(self.request, profile)
        return profile

    def get(self, request, pk):
        profile = self.get_object(pk)
        serializer = ProfileSerializer(
            profile, context={'request': request}
            )
        return Response(serializer.data)

    # We use put to update a single profile
    def put(self, request, pk):
        profile = self.get_object(pk)
        serializer = ProfileSerializer(
            profile, data=request.data, context={'request': request}
            )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        # if the serializer is not valid, return a 400 error
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
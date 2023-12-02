from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Profile
from .serializers import ProfileSerializer

class ProfileView(APIView):
    # We use get to retrieve all the profiles
    def get(self, request):
        # get all the profiles
        profiles = Profile.objects.all()
        # we need to serialize the data before sending it
        # and we set many to True because we are sending multiple objects
        serializer = ProfileSerializer(profiles, many=True)
        # return the serialized data (NOT THE OBJECTS!)
        return Response(serializer.data)

class ProfileDetail(APIView):
    # We use get_object to retrieve a single profile
    def get_object(self, pk):
        return get_object_or_404(Profile, pk=pk)

    def get(self, request, pk):
        profile = self.get_object(pk)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

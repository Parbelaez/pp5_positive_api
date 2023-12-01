from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Profile
from .serializers import ProfileSerializer

class ProfileView(APIView):
    def get(self, request):
        # get all the profiles
        profiles = Profile.objects.all()
        # we need to serialize the data before sending it
        # and we set many to True because we are sending multiple objects
        serializer = ProfileSerializer(profiles, many=True)
        # return the serialized data (NOT THE OBJECTS!)
        return Response(serializer.data)

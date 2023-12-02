from rest_framework import serializers
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    # The owner.username dot notation is used to access the username field of
    # the owner relationship
    # This can be better understood by looking at the Entities Relationship
    # Diagram in the readme file.
    owner = serializers.ReadOnlyField(source='owner.username')
    
    class Meta: 
        model = Profile
        fields = [
            ## the id field is created automatically by django
            ## but we need to declare it here to be able to access it
            'id',
            'owner',
            'created_at',
            'updated_at',
            'name',
            'content',
            'image',
        ]
from dj_rest_auth.serializers import UserDetailsSerializer
from rest_framework import serializers


class CurrentUserDetailSerializer(UserDetailSerializer):
    profile_id = serializers.IntegerField(source='profile.id')
    profile_image = serializers.ImageField(source='profile.image.url')

    class Meta(UserDetailSerializer.Meta):
        fields = UserDetailSerializer.Meta.fields + (
            'profile_id', 'profile_image'
        )
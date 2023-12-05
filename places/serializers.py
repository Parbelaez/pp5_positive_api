from rest_framework import serializers
from .models import Place


class PlaceSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Place
        fields = '__all__'
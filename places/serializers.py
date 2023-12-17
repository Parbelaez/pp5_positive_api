from rest_framework import serializers
from .models import Place


class PlaceSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    def validate(self, data):
        if Place.objects.filter(place_name=data["place_name"], city=data["city"]).count() > 0:
            raise serializers.ValidationError("A place with this name and city already exists.")
        return data

    class Meta:
        model = Place
        fields = '__all__'
from rest_framework.serializers import ModelSerializer
from .models import Trees, Section, Lot, Geolocation


class TreesSerializer(ModelSerializer):
    class Meta:
        model = Trees
        fields = '__all__'


class SectionSerializer(ModelSerializer):
    class Meta:
        model = Section
        fields = '__all__'


class LotSerializer(ModelSerializer):
    class Meta:
        model = Lot
        fields = '__all__'


class GeolocationSerializer(ModelSerializer):
    class Meta:
        model = Geolocation
        fields = '__all__'

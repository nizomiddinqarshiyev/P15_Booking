from rest_framework import serializers

from main.models import Stay, Location, City, Country, Image


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ('name',)


class CitySerializer(serializers.ModelSerializer):
    country_id = CountrySerializer()

    class Meta:
        model = City
        fields = ('name', 'country_id')


class LocationSerializer(serializers.ModelSerializer):
    city = CitySerializer()

    class Meta:
        model = Location
        fields = ('address', 'city')


class StaySimpleSerializer(serializers.ModelSerializer):
    location = LocationSerializer()

    class Meta:
        model = Stay
        fields = '__all__'




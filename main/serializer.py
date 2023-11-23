from rest_framework import serializers

from main.models import Stay, StayOrder, Flight, FlightOrder, CarRental, CarRentalOrder, Country, City, Location


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ('name', )


class CitySerializer(serializers.ModelSerializer):
    country = CountrySerializer()

    class Meta:
        model = City
        fields = ('name', 'country')


class LocationSerializer(serializers.ModelSerializer):
    city = CitySerializer()

    class Meta:
        model = Location
        fields = ('address', 'city')


class StaysSerializer(serializers.ModelSerializer):
    location = LocationSerializer()

    class Meta:
        model = Stay
        fields = '__all__'


class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = '__all__'


class CarRentalSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarRental
        fields = '__all__'


class StayOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = StayOrder
        fields = '__all__'


class FlightOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlightOrder
        fields = '__all__'


class CarRentalOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarRentalOrder
        fields = '__all__'

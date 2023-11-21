import datetime
from datetime import timedelta

from rest_framework import serializers

from main.models import Stay, StayOrder, Flight, FlightOrder, CarRental, CarRentalOrder


class StaysSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stay
        fields = '__all__'


class FlightSerializer(serializers.ModelSerializer):
    start_city_name = serializers.CharField(source='start_city.name', read_only=True)
    end_city_name = serializers.CharField(source='end_city.name', read_only=True)

    class Meta:
        model = Flight
        fields = [
            'id',
            'name',
            'description',
            'flight_category',
            'start_date',
            'end_date',
            'price',
            'start_city_id',
            'start_city_name',
            'end_city_id',
            'end_city_name'
        ]


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


class QueryStaySerializer(serializers.Serializer):
    city_or_country = serializers.CharField()
    start_date = serializers.DateTimeField(default=datetime.datetime.now())
    end_date = serializers.DateTimeField(default=datetime.datetime.now() + timedelta(days=20))
    stay_Adults = serializers.IntegerField(default=1)
    stay_Children = serializers.IntegerField(default=0)
    stay_Room = serializers.IntegerField(default=1)


class QueryFlightSerializer(serializers.Serializer):
    start_city = serializers.CharField(max_length=100)
    end_city = serializers.CharField(max_length=100)
    start_date = serializers.DateField(default=datetime.datetime.now())
    end_date = serializers.DateField(default=datetime.datetime.now() + timedelta(days=20))

from django.db.models import Q
from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.views import get_user_model
from main.models import Stay, StayOrder, Flight, FlightOrder, CarRental, CarRentalOrder
from main.serializer import StaysSerializer, StayOrderSerializer, FlightOrderSerializer, FlightSerializer, \
    CarRentalSerializer, CarRentalOrderSerializer

User = get_user_model()


# Create your views here.

class HomeAPIView(APIView):

    def get(self, request):
        return JsonResponse({'message': 'Home'})


class StaysOrderAPIView(APIView):
    permissions_class = (IsAuthenticated,)

    def get(self, request, pk):
        stays_order = StayOrder.objects.get(pk=pk)
        stay = Stay.objects.get(pk=stays_order.stay_id)
        stay_serializer = StaysSerializer(stay)
        return Response(stay_serializer.data)

    def post(self, request, pk):
        stay = Stay.objects.get(id=pk)
        if StayOrder.objects.filter(Q(user=request.user) & Q(stay=stay)):
            return Response({'message': 'This order already added'})
        else:
            stay_order = StayOrder.objects.create(
                user=request.user,
                stay=stay
            )
            stay_order.save()
            stay_order_serializer = StayOrderSerializer(stay_order)
            return Response({'success': True, 'data': stay_order_serializer.data}, status=200)


class FlightOrderAPIView(APIView):
    permissions_class = (IsAuthenticated,)

    def get(self, request, pk):
        flight = Flight.objects.get(pk=pk)
        flight_serializer = FlightSerializer(flight)
        return Response(flight_serializer.data)

    def post(self, request, pk):
        user = User.objects.get(user=request.user)
        flight_order = FlightOrder.objects.create(
            user_id=user,
            flight_id=pk
        )
        flight_order.save()
        flight_order_serializer = FlightOrderSerializer(flight_order)
        return Response({'success': True, 'data': flight_order_serializer.data}, status=200)


class CarRentalOrderAPIView(APIView):
    permissions_class = (IsAuthenticated,)

    def get(self, request, pk):
        car_rental = CarRental.objects.get(pk=pk)
        car_rental_serializer = CarRentalSerializer(car_rental)
        return Response(car_rental_serializer.data)

    def post(self, request, pk):
        user = User.objects.get(user=request.user)
        car_rental_order = CarRentalOrder.objects.create(
            user_id=user,
            flight_id=pk
        )
        car_rental_order.save()
        car_rental_order_serializer = CarRentalOrderSerializer(car_rental_order)
        return Response({'success': True, 'data': car_rental_order_serializer.data}, status=200)

import json

from django.db.models import Q
from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.views import get_user_model
from main.models import Stay, StayOrder, Flight, FlightOrder, CarRental, CarRentalOrder, City
from main.serializer import StaysSerializer, StayOrderSerializer, FlightOrderSerializer, FlightSerializer, \
    CarRentalSerializer, CarRentalOrderSerializer, QueryStaySerializer, QueryFlightSerializer

User = get_user_model()


# Create your views here.

class HomeAPIView(APIView):

    def get(self, request):
        return JsonResponse({'message': 'Home'})


class StaysOrderAPIView(APIView):
    permissions_class = (IsAuthenticated,)

    def get(self, request, pk):
        stay = Stay.objects.get(pk=pk)
        stay_serializer = StaysSerializer(stay)
        return Response(stay_serializer.data)

    def post(self, request, pk):
        user = User.objects.get(user=request.user)
        stay_order = StayOrder.objects.create(
            user_id=user.id,
            stay_id=pk
        )
        stay_order.save()
        stay_order_serializer = StayOrderSerializer(stay_order)
        return Response({'success': True, 'data': stay_order_serializer.data}, status=200)

    def delete(self, request, pk):
        StayOrder.objects.get(pk=pk).delete()
        return Response(status=204)


class FlightOrderAPIView(APIView):
    permissions_class = (IsAuthenticated,)

    def get(self, request, pk):
        flight_category = request.GET.get('flight_category', None)
        flight = None
        if flight_category:
            flight = Flight.objects.get(Q(pk=pk) & Q(flight_category=flight_category))
        else:
            flight = Flight.objects.get(pk=pk)
        flight_serializer = FlightSerializer(flight)
        return Response(flight_serializer.data)

    def post(self, request, pk):
        user = User.objects.get(user=request.user)
        flight_order = FlightOrder.objects.create(
            user_id=user.id,
            flight_id=pk
        )
        flight_order.save()
        flight_order_serializer = FlightOrderSerializer(flight_order)
        return Response({'success': True, 'data': flight_order_serializer.data}, status=200)

    def delete(self, request, pk):
        FlightOrder.objects.get(pk=pk).delete()
        return Response(status=204)


class CarRentalOrderAPIView(APIView):
    permissions_class = (IsAuthenticated,)

    def get(self, request, pk):
        car_rental = CarRental.objects.get(pk=pk)
        car_rental_serializer = CarRentalSerializer(car_rental)
        return Response(car_rental_serializer.data)

    def post(self, request, pk):
        user = User.objects.get(user=request.user)
        car_rental_order = CarRentalOrder.objects.create(
            user_id=user.id,
            flight_id=pk
        )
        car_rental_order.save()
        car_rental_order_serializer = CarRentalOrderSerializer(car_rental_order)
        return Response({'success': True, 'data': car_rental_order_serializer.data}, status=200)

    def delete(self, request, pk):
        CarRentalOrder.objects.get(pk=pk).delete()
        return Response(status=204)


class StaySearchView(GenericAPIView):
    permission_classes = ()
    serializer_class = StaysSerializer

    @swagger_auto_schema(query_serializer=QueryStaySerializer)
    def get(self, request):
        city_or_country = request.GET.get('city_or_country')
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        stay_adults = request.GET.get('stay_Adults')
        stay_children = request.GET.get('stay_Children')
        stay_room = request.GET.get('stay_Room')
        data_stays = Stay.objects.filter(
            Q(location__city__name__icontains=city_or_country) |
            Q(location__country__name__icontains=city_or_country) |
            Q(start_date=start_date, end_date=end_date) |
            Q(stay_Adults=stay_adults, stay_Children=stay_children, stay_Room=stay_room)
        ).values('id')
        stays = Stay.objects.filter(id__in=data_stays)
        stay_serializer = StaysSerializer(stays, many=True)
        if not stays:
            return Response({'error': 'Stay not fount !'}, status=404)
        return Response(stay_serializer.data)


class FlightSearchView(GenericAPIView):
    permission_classes = ()
    serializer_class = FlightSerializer

    @swagger_auto_schema(query_serializer=QueryFlightSerializer)
    def get(self, request):
        start_city = request.GET.get('start_city')
        end_city = request.GET.get('end_city')
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        data_flight = Flight.objects.filter(
            Q(start_city__name__icontains=start_city) &
            Q(end_city__name__icontains=end_city) |
            Q(start_date=start_date, end_date=end_date)
        ).values('id')
        flight = Flight.objects.filter(id__in=data_flight)
        flight_serializer = FlightSerializer(flight, many=True)
        if not flight:
            return Response({'error': 'Flight not fount !'}, status=404)
        return Response(flight_serializer.data)

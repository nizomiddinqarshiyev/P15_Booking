from rest_framework.generics import CreateAPIView, GenericAPIView
from .permissions import AdminPermission
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.views import get_user_model
from main.models import Stay, StayOrder, Flight, FlightOrder, CarRental, CarRentalOrder, Location, Image
from main.serializer import StaysSerializer, StayOrderSerializer, FlightOrderSerializer, FlightSerializer, \
    CarRentalSerializer, CarRentalOrderSerializer

User = get_user_model()


class HomeAPIView(APIView):

    def get(self, request):
        return JsonResponse({'message': 'Home'})


class StayAPIView(GenericAPIView):
    permission_classes = ()
    serializer_class = StaysSerializer

    def get(self, request, pk):
        location = Location.objects.get(pk=pk)
        base = Stay.objects.filter(location=location)
        image_data = []
        for stay in base:
            img = Image.objects.filter(stay=stay).first()
            if img:
                image_data.append({
                    'stay_id': stay.id,
                    'image_url': request.build_absolute_uri(img.image.url)
                })
        serializer_data = StaysSerializer(base, many=True).data
        response_data = {
            'stay_info': serializer_data,
            'images': image_data
        }

        return Response(response_data)


class UpdateStayAPIView(GenericAPIView):
    permission_classes = (AdminPermission,)
    serializer_class = StaysSerializer

    def put(self, request, pk):
        name = request.POST.get('name')
        description = request.POST.get('description')
        feature = request.POST.get('features')
        price = request.POST.get('price')
        property_rate = request.POST.get('property_rate')
        level = request.POST.get('level')
        location = Location.objects.get(pk=pk)
        stay = Stay.objects.get(location=location)
        stay.name = name
        stay.description = description
        stay.features = feature
        stay.price = price
        stay.property_rate_stars = property_rate
        stay.level = level
        stay.save()
        stay_serializer = StaysSerializer(stay)
        return Response(stay_serializer.data)

    def patch(self, request, pk):
        name = request.POST.get('name', None)
        description = request.POST.get('description', None)
        feature = request.POST.get('features', None)
        price = request.POST.get('price', None)
        property_rate = request.POST.get('property_rate', None)
        level = request.POST.get('level', None)
        location = Location.objects.get(pk=pk)
        stay = Stay.objects.get(location=location)
        if name:
            stay.name = name
        if description:
            stay.description = description
        if feature:
            stay.features = feature
        if price:
            stay.price = price
        if property_rate:
            stay.property_rate_stars = property_rate
        if level:
            stay.level = level
        stay.save()
        stay_serializer = StaysSerializer(stay)
        return Response(stay_serializer.data)

    def delete(self, request, pk):
        location = Location.objects.get(pk=pk)
        Stay.objects.get(location=location).delete()
        return Response(status=204)


class CreateStayAPIView(CreateAPIView):
    queryset = Stay.objects.all()
    permission_classes = (AdminPermission,)
    serializer_class = StaysSerializer


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


class StaysOrderAPIView(APIView):
    permissions_class = (IsAuthenticated,)

    def get(self, request, pk):
        stay = Stay.objects.get(pk=pk)
        stay_serializer = StaysSerializer(stay)
        return Response(stay_serializer.data)

    def post(self, request, pk):

        user = User.objects.get(user=request.user)
        stay_order = StayOrder.objects.create(
            user_id=user,
            stay_id=pk
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






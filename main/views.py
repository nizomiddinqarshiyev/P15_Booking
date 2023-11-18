from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, GenericAPIView

from .models import Stay, Category, Location, Image
from main.serializers import StaySimpleSerializer
from .permissions import AdminPermission


class StayAPIView(GenericAPIView):
    permission_classes = ()
    serializer_class = StaySimpleSerializer

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
        serializer_data = StaySimpleSerializer(base, many=True).data
        response_data = {
            'stay_info': serializer_data,
            'images': image_data
        }

        return Response(response_data)


class UpdateStayAPIView(GenericAPIView):
    permission_classes = (AdminPermission,)
    serializer_class = StaySimpleSerializer

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
        stay_serializer = StaySimpleSerializer(stay)
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
        stay_serializer = StaySimpleSerializer(stay)
        return Response(stay_serializer.data)

    def delete(self, request, pk):
        location = Location.objects.get(pk=pk)
        Stay.objects.get(location=location).delete()
        return Response(status=204)


class CreateStayAPIView(CreateAPIView):
    queryset = Stay.objects.all()
    permission_classes = (AdminPermission,)
    serializer_class = StaySimpleSerializer


class StayDetailAPIView(APIView):
    def get(self, request, slug):
        try:
            stay = Stay.objects.filter(slug=slug)
        except Stay.DoesNotExist:
            return Response({'success: False'}, status=404)
        stay_serializer = StaySimpleSerializer(stay, many=True)
        return Response(stay_serializer.data)

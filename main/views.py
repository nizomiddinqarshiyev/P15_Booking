import datetime

from django_elasticsearch_dsl_drf.constants import SUGGESTER_COMPLETION
from rest_framework.generics import CreateAPIView, GenericAPIView

from django.db.models import Q
from rest_framework.pagination import PageNumberPagination

from .documents import DocumentBlog
from .permissions import AdminPermission
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.views import get_user_model


from .models import Stay, StayOrder, Flight, FlightOrder, CarRental, CarRentalOrder, Location, Image, Comment
from .serializer import (
    StaysSerializer, StayOrderSerializer, FlightOrderSerializer, FlightSerializer,
    CarRentalSerializer, CarRentalOrderSerializer, StaySerializerFilter, CommentSerializer, QueryStaySerializer,
    QueryFlightSerializer, BlogDocumentSerializer
)

from drf_yasg.utils import swagger_auto_schema
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
from django_elasticsearch_dsl_drf.filter_backends import (
    FilteringFilterBackend,
    SearchFilterBackend,
    SuggesterFilterBackend,
)

User = get_user_model()

class CustomPageNumberPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class TodoSearchViewSet(DocumentViewSet):
    document = DocumentBlog
    serializer_class = BlogDocumentSerializer
    pagination_class = CustomPageNumberPagination

    filter_backends = [
        FilteringFilterBackend,
        SearchFilterBackend,
        SuggesterFilterBackend,
    ]

    search_fields = (
        'title',
        'slug',
        'description',
    )

    filter_fields = {
        'title': 'title',
        'slug': 'slug',
        'description': 'description',
    }

    suggester_fields = {
        'title': {
            'field': 'title.suggest',
            'suggesters': [
                SUGGESTER_COMPLETION,
            ],
        },
        'slug': {
            'field': 'slug.suggest',
            'suggesters': [
                SUGGESTER_COMPLETION,
            ],
        },
    }

    def list(self, request, *args, **kwargs):
        search_term = self.request.query_params.get('search', '')

        # Use a Q object to build a more robust query
        query = Q('multi_match', query=search_term, fields=self.search_fields)

        # Apply the query to the queryset
        queryset = self.filter_queryset(self.get_queryset().query(query))
        print('Queryset >>>>>', queryset)

        # Perform pagination
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class HomeAPIView(APIView):

    def get(self, request):
        return JsonResponse({'message': 'Home'})


class StayAPIView(GenericAPIView):
    permission_classes = ()
    serializer_class = StaysSerializer

    def get(self, request, pk):
        location = Location.objects.get(pk=pk)
        base = Stay.objects.filter(location=location)
        comment = Comment.objects.filter(stay=base)
        rate = sum(list(map(lambda t: t.rate, comment))) / len(comment)
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
            'images': image_data,
            'rate': rate
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


class StayFilterView(GenericAPIView):
    permission_classes = ()
    serializer_class = StaysSerializer
    queryset = Stay.objects.all()

    @swagger_auto_schema(query_serializer=StaySerializerFilter)
    def get(self, request):
        name = self.request.query_params.get('name', '')
        recommend = self.request.query_params.get('recommendation', '')
        category_name = self.request.query_params.get('category_name', '')
        rate = self.request.query_params.get('rate', None)

        filters = Q()

        if name:
            filters &= Q(name__icontains=name)

        if recommend:
            filters &= Stay.objects.filter(property_rate_stars__gte=6)

        if category_name:
            filters &= Q(category__name__icontains=category_name)

        if rate is not None:
            filters &= Q(property_rate_stars=rate)

        stays = self.queryset.filter(filters)

        serializer = StaysSerializer(stays, many=True)
        return Response(serializer.data)


class StaysOrderAPIView(APIView):
    permissions_class = (IsAuthenticated,)

    def get(self, request, pk):
        stay = Stay.objects.get(pk=pk)
        stay_serializer = StaysSerializer(stay)
        return Response(stay_serializer.data)

    def post(self, request, pk):
        if not StayOrder.objects.get(Q(user=request.user) & Q(stay=pk)):
            stay_order = StayOrder.objects.create(
                user=request.user,
                stay=pk
            )
            stay_order.save()
        else:
            return Response({'success': False, 'error': 'stay already exists !'})
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
        if not FlightOrder.objects.get(Q(user=request.user) & Q(flight=pk)):
            flight_order = FlightOrder.objects.create(
                user=request.user,
                flight=pk
            )
            flight_order.save()
        else:
            return Response({'success': False, 'error': 'flight already exists !'})
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
        if not CarRentalOrder.objects.get(Q(user=request.user)&Q(car_rental=pk)):
            car_rental_order = CarRentalOrder.objects.create(
                user=request.user,
                car_rental=pk
            )
            car_rental_order.save()
        else:
            return Response({'success': False, 'error': 'car_rental already exists !'})
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


class CommentAPIView(GenericAPIView):

    def get(self, request, pk):
        stay = Stay.objects.get(pk=pk)
        comments = Comment.objects.filter(stay=stay)
        comment_serializer = CommentSerializer(comments, many=True)
        print(comment_serializer)
        return Response(comment_serializer.data)


class CreateCommentAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CommentSerializer

    def post(self, request, pk):
        stay = Stay.objects.get(pk=pk)
        comment = request.data.get('comment')
        rate = request.data.get('rate')
        user_comment = Comment.objects.get(Q(user=request.user) & Q(stay=stay))
        if not user_comment:
            comments = Comment.objects.create(
                comment=comment,
                rate=rate,
                created_at=datetime.datetime.now(),
                user=request.user,
                stay=stay
            )
        else:
            comments = Comment.objects.create(
                comment=comment,
                rate=user_comment.rate,
                created_at=datetime.datetime.now(),
                user=request.user,
                stay=stay
            )
        comments.save()
        comment_serializer = CommentSerializer(comments)
        return JsonResponse(comment_serializer.data)


class CommentUpdateAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = CommentSerializer

    def patch(self, request, pk):
        comment_data = Comment.objects.get(Q(user=request.user) & Q(pk=pk))
        comment_rate = Comment.objects.filter(Q(user=request.user) & Q(stay=comment_data.stay))
        comment = request.data.get('comment')
        rate = request.data.get('rate')
        print(comment_rate)

        if comment:
            comment_data.comment = comment
            comment_data.save()
        if rate:
            comment_rate.update(rate=rate)

        comment_serializer = CommentSerializer(comment_data)
        return Response(comment_serializer.data)

    def delete(self, request, pk):
        Comment.objects.get(Q(user=request.user) & Q(pk=pk)).delete()
        return Response(status=204)

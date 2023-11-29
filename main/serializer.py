from datetime import datetime, timedelta

from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from rest_framework import serializers

from main.documents import DocumentStay
from main.models import Stay, StayOrder, Flight, FlightOrder, CarRental, CarRentalOrder, Country, City, Location, \
    Category, Comment, Subscriber, Blog
from main.tasks import send_email


class StaySerializerFilter(serializers.Serializer):
    recommend = serializers.CharField(required=False)
    name = serializers.CharField(required=False)
    category_name = serializers.CharField(required=False)
    level = serializers.IntegerField(required=False)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name',)


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ('name',)


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
    category = CategorySerializer()

    class Meta:
        model = Stay
        fields = '__all__'


class StayCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stay
        fields = '__all__'


class QuerySerializer(serializers.Serializer):
    query = serializers.CharField()


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


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('rate', 'comment')


class QueryStaySerializer(serializers.Serializer):
    city_or_country = serializers.CharField()
    start_date = serializers.DateTimeField(default=datetime.now())
    end_date = serializers.DateTimeField(default=datetime.now() + timedelta(days=20))
    stay_Adults = serializers.IntegerField(default=1)
    stay_Children = serializers.IntegerField(default=0)
    stay_Room = serializers.IntegerField(default=1)


class QueryFlightSerializer(serializers.Serializer):
    start_city = serializers.CharField(max_length=100)
    end_city = serializers.CharField(max_length=100)
    start_date = serializers.DateField(default=datetime.now())
    end_date = serializers.DateField(default=datetime.now() + timedelta(days=20))


class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscriber
        fields = '__all__'


class StayDocumentSerializer(DocumentSerializer):
    class Meta:
        document = DocumentStay
        fields = ('title', 'slug', 'description')


class SlugSerializer(serializers.Serializer):
    slug = serializers.CharField()


class BlogSerializerForRetrieve(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = '__all__'


class BlogSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        subscribers = Subscriber.objects.all().values('email')
        subscriber_emails = [email['email'] for email in list(subscribers)]
        print(subscriber_emails)
        todo = Blog.objects.create(**validated_data)
        todo_serializer = BlogSerializerForRetrieve(todo)
        send_email.delay(subscriber_emails, todo_serializer.data)
        return todo

    class Meta:
        model = Blog
        fields = '__all__'

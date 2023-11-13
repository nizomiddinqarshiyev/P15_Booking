from django.contrib.auth.views import get_user_model
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

User = get_user_model()

class Category(MPTTModel):
    name = models.CharField(max_length=50)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)


class Country(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Country'
        verbose_name_plural = 'Counties'

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=50)
    country_id = models.ForeignKey('Country', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'City'
        verbose_name_plural = 'Cities'

    def __str__(self):
        return self.name


class Location(models.Model):
    lat = models.FloatField()
    lon = models.FloatField()
    city = models.ForeignKey('City', on_delete=models.CASCADE)
    country = models.ForeignKey('Country', on_delete=models.CASCADE)
    address = models.CharField(max_length=150)
    location = models.FloatField()


class Stay(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    category_id = models.ForeignKey('Category', on_delete=models.CASCADE)
    location = models.ForeignKey('Location', on_delete=models.CASCADE)
    features = models.TextField(blank=True, null=True)
    price = models.FloatField()
    property_rate_stars = models.IntegerField()
    level = models.IntegerField(default=0)


class CarRental(models.Model):
    name = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    location = models.ForeignKey('Location', on_delete=models.CASCADE)
    price = models.FloatField()


class Flight(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    price = models.FloatField()


class StayOrder(models.Model):
    stay_id = models.ForeignKey('Stay', on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    last_update = models.DateTimeField(auto_now_add=True)


class FlightOrder(models.Model):
    flight_id = models.ForeignKey('Flight', on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    last_update = models.DateTimeField(auto_now_add=True)


class CarRentalOrder(models.Model):
    car_rental = models.ForeignKey('CarRental', on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    last_update = models.DateTimeField(auto_now_add=True)

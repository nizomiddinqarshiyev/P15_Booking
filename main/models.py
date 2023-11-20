from datetime import datetime
from django.contrib.auth.views import get_user_model

from django.db import models
from os.path import splitext
from django.template.defaultfilters import slugify
from mptt.models import MPTTModel, TreeForeignKey


User = get_user_model()

def slugify_upload(instance, filename):
    folder = instance._meta.model_name
    name, ext = splitext(filename)
    name_t = slugify(name) or name
    return f"{folder}/{name_t}{ext}"


class Image(models.Model):
    image = models.ImageField(upload_to=slugify_upload, blank=True, null=True)
    stay = models.ForeignKey('main.Stay', on_delete=models.CASCADE)


class Category(MPTTModel):
    name = models.CharField(max_length=50)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)


class Country(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'

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
    slug = models.SlugField(blank=True, null=True)
    price = models.FloatField()
    property_rate_stars = models.IntegerField()
    level = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


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
    stay = models.ForeignKey('Stay', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    last_update = models.DateTimeField(auto_now_add=True)


class FlightOrder(models.Model):
    flight = models.ForeignKey('Flight', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    last_update = models.DateTimeField(auto_now_add=True)


class CarRentalOrder(models.Model):
    car_rental = models.ForeignKey('CarRental', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    last_update = models.DateTimeField(auto_now_add=True)


class HotelAreaInfo(models.Model):
    name = models.CharField(max_length=50)
    stay = models.ForeignKey('Stay', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    distance = models.FloatField()

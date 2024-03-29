from os.path import splitext
from django.template.defaultfilters import slugify

from django.contrib.auth.views import get_user_model
from django.db import models

from mptt.models import MPTTModel, TreeForeignKey

User = get_user_model()


def slugify_upload(instance, filename):
    folder = instance._meta.model_name
    name, ext = splitext(filename)
    name_t = slugify(name) or name
    return f"{folder}/{name_t}{ext}"


class Category(MPTTModel):
    name = models.CharField(max_length=50)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=50)
    country = models.ForeignKey('Country', on_delete=models.CASCADE)

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

    def __str__(self):
        return self.address


class Stay(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    location = models.ForeignKey('Location', on_delete=models.CASCADE)
    features = models.TextField(blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)
    price = models.FloatField()
    level = models.IntegerField(default=0)
    room = models.IntegerField(default=0, null=True, blank=True)
    adults = models.IntegerField(default=0, null=True, blank=True)
    children = models.IntegerField(default=0, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class CarRental(models.Model):
    name = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    location = models.ForeignKey('Location', on_delete=models.CASCADE)
    price = models.FloatField()
    image = models.ImageField(upload_to=slugify_upload, blank=True, null=True)

    def __str__(self):
        return self.name


class Flight(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    price = models.FloatField()

    logo = models.ImageField(upload_to=slugify_upload, blank=True, null=True)

    def __str__(self):
        return self.name


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


class Image(models.Model):
    stay = models.ForeignKey('Stay', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=slugify_upload, blank=True, null=True)


class Comment(models.Model):
    comment = models.TextField()
    rate = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stay = models.ForeignKey(Stay, on_delete=models.CASCADE, blank=True, null=True)


class Blog(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField(blank=True, null=True)
    description = models.TextField()
    expires_at = models.DateTimeField(auto_now_add=True)

    def save(
        self, *args, **kwargs
    ):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Subscriber(models.Model):
    email = models.EmailField()
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


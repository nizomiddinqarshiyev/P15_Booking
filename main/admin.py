from django.contrib import admin

from main.models import (
    Category,
    Stay,
    City,
    Country,
    CarRental,
    Location,
    CarRentalOrder,
    Flight,
    FlightOrder,
    HotelAreaInfo,
    Image
)

admin.site.register((Category, Stay,
                     City, Country,
                     CarRental, Location,
                     CarRentalOrder,
                     Flight, FlightOrder,
                     HotelAreaInfo, Image,))

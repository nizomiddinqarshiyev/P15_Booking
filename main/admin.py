from django.contrib import admin

from main.models import Stay, Flight, CarRental, Location, City, Country, Category

admin.site.register((Stay, Flight, CarRental, Location, City, Country, Category))

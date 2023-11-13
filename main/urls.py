from django.urls import path
from .views import HomeAPIView, StaysOrderAPIView, FlightOrderAPIView, CarRentalOrderAPIView

urlpatterns = [
    path('', HomeAPIView.as_view(), name='home'),
    path('stay-order<int:pk>', StaysOrderAPIView.as_view(), name='stay_order'),
    path('flight-order<int:pk>', FlightOrderAPIView.as_view(), name='flight_order'),
    path('car-rental<int:pk>', CarRentalOrderAPIView.as_view(), name='car_rental_order'),
]
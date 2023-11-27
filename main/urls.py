from django.urls import path
from .views import (StayAPIView, CreateStayAPIView, UpdateStayAPIView, StayFilterView, HomeAPIView,
                    StaysOrderAPIView,
                    FlightOrderAPIView,
                    CarRentalOrderAPIView
)


urlpatterns = [
    path('', HomeAPIView.as_view(), name='home'),
    path('stay-order/<int:pk>', StaysOrderAPIView.as_view(), name='stay_order'),
    path('flight-order/<int:pk>', FlightOrderAPIView.as_view(), name='flight_order'),
    path('car-rental/<int:pk>', CarRentalOrderAPIView.as_view(), name='car_rental_order'),
    path('stays/<int:pk>', StayAPIView.as_view(), name='stays'),
    path('update/<int:pk>', UpdateStayAPIView.as_view(), name='update'),
    path('filters', StayFilterView.as_view(), name='filters'),
    path('create-stay', CreateStayAPIView.as_view(), name='create_stay'),
    path('stay-order/<int:pk>', StaysOrderAPIView.as_view(), name='stay_order'),
    path('flight-order/<int:pk>', FlightOrderAPIView.as_view(), name='flight_order'),
    path('car-rental/<int:pk>', CarRentalOrderAPIView.as_view(), name='car_rental_order'),
]


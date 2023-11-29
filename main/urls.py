from django.urls import path, include
from .views import (StayAPIView, CreateStayAPIView, UpdateStayAPIView, StayFilterView, HomeAPIView,
                    StaysOrderAPIView,
                    FlightOrderAPIView,
                    CarRentalOrderAPIView, CommentUpdateAPIView, CommentAPIView,
                    CreateCommentAPIView, BlogUpdateAPIView, CreateBlogAPIView, SubscribeAPIView, StaySearchAPIView,
                    LocationAPIView, FlightSearchView, StaySearchElasticAPIView
                    )
from rest_framework import routers

router = routers.DefaultRouter(trailing_slash=False)
router.register('elastic-search', StaySearchElasticAPIView, basename='elastic_search')


urlpatterns = [
    path('', HomeAPIView.as_view(), name='home'),
    path('stay-order/<int:pk>', StaysOrderAPIView.as_view(), name='stay_order'),
    path('flight-order/<int:pk>', FlightOrderAPIView.as_view(), name='flight_order'),
    path('car-rental/<int:pk>', CarRentalOrderAPIView.as_view(), name='car_rental_order'),
    path('stays/<int:pk>', StayAPIView.as_view(), name='stays'),
    path('stay-update/<int:pk>', UpdateStayAPIView.as_view(), name='update'),
    path('filters', StayFilterView.as_view(), name='filters'),
    path('create-stay', CreateStayAPIView.as_view(), name='create_stay'),
    path('stay-order/<int:pk>', StaysOrderAPIView.as_view(), name='stay_order'),
    path('flight-order/<int:pk>', FlightOrderAPIView.as_view(), name='flight_order'),
    path('car-rental/<int:pk>', CarRentalOrderAPIView.as_view(), name='car_rental_order'),
    path('comment/<int:pk>', CommentAPIView.as_view(), name='comment'),
    path('create-comment/<int:pk>', CreateCommentAPIView.as_view(), name='create_comment'),
    path('comment-update/<int:pk>', CommentUpdateAPIView.as_view(), name='comment_update'),
    path('stay-order/<int:pk>', StaysOrderAPIView.as_view(), name='stay_order'),
    path('flight-order/<int:pk>', FlightOrderAPIView.as_view(), name='flight_order'),
    path('car-rental/<int:pk>', CarRentalOrderAPIView.as_view(), name='car_rental_order'),
    path('blog-update/<int:pk>', BlogUpdateAPIView.as_view(), name='blog_update'),
    path('create-blog', CreateBlogAPIView.as_view(), name='create_blog'),
    path('subscribe', SubscribeAPIView.as_view(), name='subscribe'),
    path('stay-search', StaySearchAPIView.as_view(), name='stay_search'),
    path('location/<int:pk>', LocationAPIView.as_view(), name='location'),
    path('flight-search', FlightSearchView.as_view(), name='flight_search')
    # path('', include(router.urls))
]


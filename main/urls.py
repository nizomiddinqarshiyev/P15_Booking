from django.urls import path
from .views import StayAPIView, UpdateStayAPIView, CreateStayAPIView

urlpatterns = [
    path('stays/<int:pk>', StayAPIView.as_view(), name='stays'),
    path('update/<int:pk>', UpdateStayAPIView.as_view(), name='update'),
    path('create-stay', CreateStayAPIView.as_view(), name='create_stay')
]

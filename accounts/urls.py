
from django.urls import path

from .views import LoginAPIVew, LogoutAPIVew, SignupAPIView

urlpatterns = [
    path('login/', LoginAPIVew.as_view(), name='login'),
    path('signup/', SignupAPIView.as_view(), name='signup'),
    path('logout/', LogoutAPIVew.as_view(), name='logout'),
]



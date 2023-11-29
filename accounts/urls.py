
from django.urls import path

from .views import SignupAPIView, LogoutAPIVew, UserInfoAPIView

urlpatterns = [
    path('signup/', SignupAPIView.as_view(), name='signup'),
    path('logout/', LogoutAPIVew.as_view(), name='logout'),
    path('user-info/', UserInfoAPIView.as_view(), name='user')
]



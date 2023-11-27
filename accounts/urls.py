
from django.urls import path

from .views import SignupAPIView

urlpatterns = [
    path('signup/', SignupAPIView.as_view(), name='signup'),
    # path('logout/', LogoutAPIVew.as_view(), name='logout'),
]



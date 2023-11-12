from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import hashers, login, logout, authenticate
from .serializer import UserSerializer

User = get_user_model()


class SignupAPIView(APIView):

    def get(self, request):
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 == password2:
            if User.objects.filter(usernmae=username).exists():
                return Response({'success' : False, 'error' : 'Username already exists !' }, status = 400)
            if User.objects.filter(email=email).exists():
                return Response({'success' : False, 'error' : 'Email already exists !' }, status = 400)

            user = User.objects.create(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                password=hashers.make_password(password2)
            )
            user_serializer = UserSerializer(user)
            return Response({'success' : True, 'data' : user_serializer.data})

        else:
            return Response({'success' : False, 'error' : 'Passwords are not same !!!'})


class LoginAPIVew(APIView):

    def get(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return Response({'success' : True })
        else:
            return Response({'success' : False, 'error' : 'Username or password invalid !!!'})


class LogoutAPIVew(APIView):

    def get(self, request):
        logout(request)
        return Response()







from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import hashers, login, logout, authenticate
from .serializer import UserSerializer

User = get_user_model()


class SignupAPIView(APIView):

    def post(self, request):
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                return Response({'success': False, 'error': 'Username already exists !'}, status=400)
            if User.objects.filter(email=email).exists():
                return Response({'success': False, 'error': 'Email already exists !'}, status=400)

            user = User.objects.create_user(
                first_name=firstname,
                last_name=lastname,
                username=username,
                email=email,
                password=password1
            )
            user_serializer = UserSerializer(user)
            return Response({'success': True, 'data': user_serializer.data})

        else:
            return Response({'success': False, 'error': 'Passwords are not same !!!'})


class LoginAPIVew(APIView):

    def get(self, request):
        username = request.GET.get('username')
        password = request.GET.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return Response({'success': True}, )
        else:
            return Response({'success': False, 'error': 'Username or password invalid !!!'})


class LogoutAPIVew(APIView):

    def get(self, request):
        logout(request)
        return Response()







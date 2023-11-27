from django.contrib.auth import get_user_model
from django.contrib.auth import hashers, login, logout, authenticate
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from accounts.serializer import UserSerializer, LoginSerializer
from accounts.subscriber import send_mail

User = get_user_model()


class SignupAPIView(GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        username = request.data.get('username')
        email = request.data.get('email')
        password1 = request.data.get('password1')
        password2 = request.data.get('password2')

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                return Response({'success': False, 'error': 'Error username'})
            if User.objects.filter(email=email).exists():
                return Response({'success': False, 'error': 'Error email'})
            code = send_mail(email)
            active_code = input('Active code >>> ')
            if active_code != code:
                return Response({'success': False, 'error': 'Error code'})

            user = User.objects.create(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                password=hashers.make_password(password2)
            )
            user.save()
            user_serializer = UserSerializer(user)
            return Response({'success': True, 'data': user_serializer.data})
        else:
            return Response({'success': False, 'error': 'Error password'})


class LoginAPIVew(GeneratorExit):
    serializer_class = LoginSerializer

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return Response({'success': True}, )
        else:
            return Response({'success': False, 'error': 'Username or password invalid !!!'})


class LogoutAPIVew(GeneratorExit):

    def get(self, request):
        logout(request)
        return Response()







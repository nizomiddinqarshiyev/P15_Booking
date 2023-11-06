from django.http import JsonResponse
from django.shortcuts import render
from django.views import View


class LoginView(View):

    def get(self, request):
        return JsonResponse({'message':  'Hello'})

# Create your views here.

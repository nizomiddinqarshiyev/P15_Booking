from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView


# Create your views here.

class HomeAPIView(APIView):

    def get(self, request):
        return JsonResponse({'message': 'Home'})


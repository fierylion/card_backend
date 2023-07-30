from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from .serializers import CustomUserSerializer
from .models import CustomUser

# Create your views here.
class UserView(ViewSet):
    def create_single_user(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class PaymentOperationView(ViewSet):
    def create_payment_link(self, request):
        pass
    def receive_callback(self, request):
        pass
  

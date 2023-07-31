from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from .serializers import CustomUserSerializer, TransactionSerializer, TransactionRecordsSerializer, UserDataSerializer

from .models import CustomUser, Transaction, TransactionRecords, UserData
import os
from azampay import Azampay
import jwt
from django.forms import model_to_dict
from .card_creation import create_card
import uuid
# Create your views here.
class UserView(ViewSet):
    def create_single_user(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user_data = serializer.data
            del user_data["password"]
            encoded_token=jwt.encode({"user_id":user_data["id"] }, os.getenv("JWT_SECRET"), algorithm="HS256")

            return Response({"data":user_data, "token":encoded_token, "status":'success'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def login_single_user(self, request):
        email = request.data.get("email")
        password=request.data.get("password")
        if(email):
            user=CustomUser.objects.filter(email=email).first()
            if(user):
                obtained_password = user.password
                if(password==obtained_password):
                    encoded_token = jwt.encode({"user_id":str(user.id) }, os.getenv("JWT_SECRET"), algorithm="HS256")
                    return Response({"data":{
                        "id":str(user.id),
                        "email":user.email,
                        "paid":user.paid

                    }, "token":encoded_token, "status":"success" }, status=status.HTTP_200_OK)
                return Response({"err":"password is not correct!", "status":"failed"}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"err":"Email doesn\'t exist!", "status":"failed"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"err":"Please provide email!"}, status=status.HTTP_400_BAD_REQUEST)
    def save_details(self, request):
        serializer=UserDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status":"success"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



class PaymentOperationView(ViewSet):
    def create_payment_link(self, request):
        provider = request.data.get("provider")
        if(provider):
            azampay = Azampay( app_name=os.environ.get('APP_NAME'), client_id=os.environ.get('CLIENT_ID'), client_secret=os.environ.get('CLIENT_SECRET_KEY'), sandbox=True)
            track = str(uuid.uuid4())
            CustomUser.objects.filter(id=request.user.id).update(reference=track)

            data = azampay.generate_payment_link(
                amount=10000,
                external_id=track,
                provider=provider
            )
            print(data)
            return Response(data, status=status.HTTP_200_OK)
        return Response({"err":"Please provide provider"}, status=status.HTTP_400_BAD_REQUEST)
    def receive_callback(self, request):
        #message, user, password, clientId, submerchantAcc, additionalProperties
        request.data.pop("message")
        request.data.pop("additionalProperties")
        request.data.pop("clientId")
        request.data.pop("password")
        request.data.pop("submerchantAcc")
        request.data.pop("user")
        request.data['user']=request.user
        serializer=TransactionSerializer(data=request.data)
        if serializer.is_valid():
            details = serializer.save()
            if(details["transactionstatus"]=="success" and details["amount"]==10000):
                CustomUser.objects.filter(reference=details['reference']).update(paid=True)
                info = UserData.objects.filter(user=request.user).first()
                card_path = create_card(data={"first_name":info.first_name,"membership_no":info.membership_no,"phone_number":info.phone_number})
                print(card_path) #email the card to the user
            return Response({"status":"success"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
            

  

from django.db import models
import uuid
# Create your models here.
class CustomUser(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email=models.EmailField(unique=True,blank=False,null=False, error_messages={
        'unique':"Email already exists, Please enter another one!",
        "blank":"Email field can\'t be blank"
    })
    password=models.CharField(max_length=400, null=False, blank=False)
    paid=models.BooleanField()

"""
q: for transaction models should have those fieldsamount
required
string
This is amount that will be charged from the given account.

currencyCode
required
string
Code of currency

merchantAccountNumber
required
string
This is the account number/MSISDN that consumer will provide. The amount will be deducted from this account.

merchantMobileNumber
required
string
Mobile number

merchantName
string or null
The name of consumer

otp
required
string
One time password

provider
required
string (BankProvider)
Enum: "CRDB" "NMB"
referenceId
string or null
This id belongs to the calling application. Maximum Allowed length for this field is 128 ascii characters
"""

class Transaction(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    amount=models.FloatField()
    currencyCode=models.CharField(max_length=3)
    merchantAccountNumber=models.CharField(max_length=20)
    merchantMobileNumber=models.CharField(max_length=20)
    merchantName=models.CharField(max_length=100)
    otp=models.CharField(max_length=6)
    provider=models.CharField(max_length=4)
    referenceId=models.CharField(max_length=128)
    user=models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

class TransactionRecords(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    amount=models.FloatField()
    currencyCode=models.CharField(max_length=3)
    merchantAccountNumber=models.CharField(max_length=20)
    merchantMobileNumber=models.CharField(max_length=20)
    merchantName=models.CharField(max_length=100)
    otp=models.CharField(max_length=6)
    provider=models.CharField(max_length=4)
    referenceId=models.CharField(max_length=128)
    user=models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)


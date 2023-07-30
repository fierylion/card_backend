from django.db import models
import uuid
# Create your models here.
class CustomUser(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name=models.CharField(max_length=225, null=False, blank=False)
    password=models.CharField(max_length=400, null=False, blank=False)
    paid=models.BooleanField()
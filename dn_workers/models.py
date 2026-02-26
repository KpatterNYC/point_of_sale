from django.db import models
from django.contrib.auth import get_user_model


class WorkerRoles(models.TextChoices):
    SELLER="seller","Seller"
    STOCKER="stocker","Stocker",
    MANAGER="manager","Manager"
    OWNER="owner","Owner"
    
    
class WorkerProfile(models.Model):
    first_name=models.CharField(max_length=100,verbose_name="Legal First Name")
    last_name=models.CharField(max_length=100,verbose_name="Legal Last Name")
    role=models.CharField(max_length=30,choices=WorkerRoles.choices,default=WorkerRoles.SELLER)
    user=models.OneToOneField(get_user_model(),related_name="worker_profile",null=True,blank=True,on_delete=models.SET_NULL)
    phone_number=models.CharField(max_length=10,verbose_name="Primary Phone Number",unique=True)
    is_active=models.BooleanField(default=False)
    is_owner=models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} "
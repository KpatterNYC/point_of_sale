import uuid
from django.db import models
from django.contrib.auth import get_user_model

from cloudinary_storage.storage import MediaCloudinaryStorage

from dn_workers import models as worker_models


class Sale(models.Model):
    class PaymentMethods(models.TextChoices):
        CASH="cash","Cash"
    sale_dt=models.DateTimeField(auto_now_add=True)
    amount_recieved=models.IntegerField()
    profit=models.IntegerField(null=True,blank=True)
    admin_handler=models.ForeignKey(get_user_model(),related_name="admin_sales",null=True,blank=True,on_delete=models.CASCADE)
    worker_handler=models.ForeignKey(worker_models.WorkerProfile,related_name="employee_sales",null=True,blank=True,on_delete=models.SET_NULL)
    payment_method=models.CharField(max_length=20, choices=PaymentMethods.choices)
    cash_amount=models.IntegerField(null=True,blank=True)
    sale_pk=models.UUIDField(default=uuid.uuid4,primary_key=True,editable=False)
    customer_name=models.CharField(max_length=100)
    customer_phone_number=models.CharField(max_length=100)
    receipt_number=models.CharField(max_length=30)
    receipt=models.FileField(upload_to="receipts/",storage=MediaCloudinaryStorage())
    
    
    def __str__(self):
        return f"Sale done {self.sale_dt} for $ {self.amount_recieved} with a profit of $ {self.profit}"
    
    @property
    def apiIdentifier(self):
        return str(self.sale_pk).replace("-","_")

class SoldProduct(models.Model):
    product_details=models.JSONField(default=dict)
    sale=models.ForeignKey(Sale,related_name="products_sold",on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Products sold for Sale instance {self.sale}"
    
class CashTracker(models.Model):
    cash_dt=models.DateField(auto_now_add=True)
    amount=models.IntegerField()
    
    def __str__(self):
        return f"{self.cash_dt} - > $ {self.amount:,}"
    
    
    
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class extenduser(models.Model):
    cash_earn=models.IntegerField(default=0)
    no_referal=models.IntegerField(default=0)
    referal=models.CharField(max_length=30)
    user=models.OneToOneField(User,on_delete=models.CASCADE)

class Order(models.Model): 
    phone=models.CharField(max_length=20)
    UPI_ID=models.CharField(max_length=30)
    paid=models.BooleanField(default=False)
    plan=models.CharField(max_length=30)
    Refer_by=models.CharField(max_length=30)
    payment_id=models.CharField(max_length=100,default='')

    


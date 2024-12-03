from django.db import models
from user.models import CustomUser


# Create your models here.

class Address(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='addresses')
    name=models.CharField(max_length=50)
    address_title=models.CharField(max_length=50,default='Home')
    state=models.CharField(max_length=100)
    city=models.CharField(max_length=100)
    pin=models.CharField(max_length=6)
    detail_address=models.TextField(null=True,blank=True)
    landmark=models.CharField(max_length=100,null=True,blank=True)
    phone_number=models.CharField(max_length=15, unique=False, null=True, blank=True)

    def __str__(self):
        return f"{self.name},{self.city},{self.state}"


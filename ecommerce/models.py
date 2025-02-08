from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumber
import datetime
class Users(AbstractUser):
    address = models.CharField(max_length=200, blank=False, null=True)
    phone = PhoneNumber(region='EU')

    def __str__(self):
        return self.address.capitalize()
    
class Categories(models.Model):
    name = models.CharField(max_length=100, null=False, unique=True, blank=False)

    def __str__(self):
        return self.name.title()

class Products(models.Model):
    category_id = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name='category')
    name = models.CharField(max_length=200, unique=True, null=False, blank=False)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    discount = models.DecimalField(max_digits=2, decimal_places=2, default=0.00)
    stock = models.IntegerField(default=0)
    image = models.URLField(blank=True, null=True)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name.capitalize()

class Orders(models.Model):
    ORDER_STATE =[
        ('pendiente','Pendiente'), 
        ('procesado','Procesando'), 
        ('enviado','Enviado'), 
        ('entregado','Entregado'), 
        ('cancelado','Cancelado')
        ]

    user_id = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='users')
    date_order = models.DateTimeField(auto_now_add=True)
    total_order = models.DecimalField(max_digits=6, decimal_places=2, null=False, blank=False)
    mailing_address = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(choices=ORDER_STATE, default=ORDER_STATE[0][0])

    def __str__(self):
        return f"{self.user_id} - {self.date_order.strftime('%Y-%m-%d')} - ${self.total_order:.2f}"




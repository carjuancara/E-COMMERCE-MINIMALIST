from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumber

class Users(AbstractUser):
    address = models.CharField(max_length=200, blank=False, null=True)
    phone = PhoneNumber(region='EU')

    def __str__(self):
        return self.address.capitalize()
    
class Categories(models.Model):
    name = models.CharField(max_length=100, null=False, unique=True, blank=False)

    def __str__(self):
        return self.name.title()





from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.text  import slugify

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    address = models.CharField(max_length=200, blank=False, null=True)
    phone = PhoneNumberField(blank=True, null=True) 
    
    def __str__(self):
        return f"Perfil de {self.user.username}"

class Categories(models.Model):
    name = models.CharField(max_length=100, null=False, unique=True, blank=False)
    slug = models.SlugField(unique=True, blank=True, null=False)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name.title()

class Products(models.Model):
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name='products', default=1)
    name = models.CharField(max_length=200, unique=True, null=False, blank=False)
    slug = models.SlugField(unique=True, blank=True, null=False)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    discount = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        validators=[MinValueValidator(0), MaxValueValidator(100)], 
        default=0
    )
    stock = models.PositiveIntegerField(default=0)
    image = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name.capitalize()

    def calculate_discount(self):
        return (self.price * self.discount) / 100

class Orders(models.Model):
    ORDER_STATE = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled')
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', default=1)
    date_ordered = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], default=0.00)
    shipping_address = models.CharField(max_length=255, null=False, blank=False)
    status = models.CharField(choices=ORDER_STATE, default='pending', max_length=20)

    def __str__(self):
        return f"Orden de {self.user.username} - {self.date_ordered.strftime('%Y-%m-%d')}"

class OrderItem(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        if not self.unit_price:
            self.unit_price = self.product.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.order.id} - {self.product.name}"

    def get_total(self):
        return self.quantity * self.unit_price
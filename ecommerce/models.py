from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.text import slugify
from decimal import Decimal

class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile', unique=True)
    address = models.CharField(max_length=200, blank=False, null=True, help_text="user address" )
    phone = PhoneNumberField(blank=True, null=True, help_text="user phone")

    def __str__(self):
        return f"Perfil de {self.user.username}"


class Categories(models.Model):
    name = models.CharField(max_length=100, null=False,
                            unique=True, blank=False, help_text='category name')
    slug = models.SlugField(unique=True, blank=True, null=False, help_text='category slug' )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name.title()


class Products(models.Model):
    category = models.ForeignKey(
        Categories, on_delete=models.CASCADE, related_name='products', default=1)
    name = models.CharField(max_length=200, unique=True,
                            null=False, blank=False, help_text='product name')
    slug = models.SlugField(unique=True, blank=True, null=False, help_text = 'product slug')
    description = models.TextField(blank=True, help_text='Brief description of the product')
    price = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal("0.00"), validators=[MinValueValidator(Decimal("0.00")), MaxValueValidator(Decimal("10000000.00"))], help_text='product price')
    discount = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00")), MaxValueValidator(Decimal("10000000.00"))],
        default=Decimal("0.00"),
        help_text='Product discount percentage'
    )
    stock = models.PositiveIntegerField(default=0, help_text='current amount')
    image = models.URLField(blank=True, null=True, help_text='image of the product')
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

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='orders', default=1)
    date_ordered = models.DateTimeField(auto_now_add=True, help_text='date of order placed')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[
                                    MinValueValidator(Decimal("0.00")), MaxValueValidator(Decimal("10000000.00"))], default=Decimal("0.00"), )
    shipping_address = models.CharField(
        max_length=255, null=False, blank=False, help_text='mailing address')
    status = models.CharField(
        choices=ORDER_STATE, default='pending', max_length=20, help_text='order status')

    def __str__(self):
        return f"Orden de {self.user.username} - {self.date_ordered.strftime('%Y-%m-%d')}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Orders, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0, help_text='quantity of units ordered of the item', validators=[MinValueValidator(0), MaxValueValidator(1000)])
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[
                                    MinValueValidator(Decimal("0.00")), MaxValueValidator(Decimal("10000000.00"))], default=Decimal("0.00"), help_text='price per unit of each product')

    def save(self, *args, **kwargs):
        if not self.unit_price:
            self.unit_price = self.product.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.order.id} - {self.product.name}"

    def get_total(self):
        return self.quantity * self.unit_price

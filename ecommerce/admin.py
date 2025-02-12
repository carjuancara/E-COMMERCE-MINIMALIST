from django.contrib import admin
from ecommerce.models import Profile, Categories, Products, Orders, OrderItem

admin.site.register(Profile)
admin.site.register(Categories)
admin.site.register(Products)
admin.site.register(Orders)
admin.site.register(OrderItem)

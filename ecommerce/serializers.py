from rest_framework.serializers import ModelSerializer
from ecommerce.models import Profile, Products, Orders, OrderItem, Categories


class ProfileSerializer(ModelSerializer):
    class Meta:
        model= Profile
        fields = ("address", "phone")

class CategoriesSerializer(ModelSerializer):
    class Meta:
        model = Categories
        fields = ("name", "slug")

class ProductsSerializer(ModelSerializer):
    class Meta:
        model = Products
        fields = ("name", "slug", "description", "price", "discount", "stock", "image", "created_at")
        read_only_fields = ("created_at",)

class OrdersSerializer(ModelSerializer):
    class Meta:
        model = Orders
        fields = ("date_ordered", "total_amount", "shipping_address", "status")
class OrderItemSerializer(ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ("quantity", "unit_price")

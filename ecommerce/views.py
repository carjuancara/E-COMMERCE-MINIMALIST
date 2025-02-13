from rest_framework.viewsets import ModelViewSet
from ecommerce.serializers import ProductsSerializer, ProfileSerializer, CategoriesSerializer, OrdersSerializer, OrderItemSerializer
from ecommerce.models import Products, Profile, Categories, Orders, OrderItem

class ProductViewSet(ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer

class ProfileViewSet(ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

class CategoryViewSet(ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer

class OrderViewSet(ModelViewSet):
    queryset = Orders.objects.all()
    serializer_class = OrdersSerializer

class OrderItemViewSet(ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

from rest_framework.routers import DefaultRouter
from django.urls import path, include
from ecommerce.views import ProductViewSet, ProfileViewSet, OrderItemViewSet, OrderViewSet, CategoryViewSet

router = DefaultRouter()
router.register(r'product', ProductViewSet)
router.register(r'profile', ProfileViewSet)
router.register(r'order', OrderViewSet)
router.register(r'orderitem', OrderItemViewSet)
router.register(r'category', CategoryViewSet)

urlpatterns = [
    path('',include(router.urls))
]
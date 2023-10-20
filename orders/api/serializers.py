from rest_framework.serializers import ModelSerializer
from ..models import OrderItem, Order

class OderItemSerializer(ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'order_id', 'product_variant_id', 'price', 'quantity', 'amount']

class OrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'user', 'full_name', 'address', 'phone', 'email', 'shipping_method', 'payment_method', 'status', 'comment']
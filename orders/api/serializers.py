from rest_framework.serializers import ModelSerializer
from ..models import OrderItem

class OderItemSerializer(ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'order_id', 'product_variant_id', 'price', 'quantity', 'amount']
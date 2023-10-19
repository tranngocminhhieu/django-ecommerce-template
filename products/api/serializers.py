from rest_framework.serializers import ModelSerializer
from ..models import ProductVariant, Product

class ProductVariantSerializer(ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = ['product', 'color', 'version', 'price', 'quantity']

class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'slug', 'description', 'image', 'brand', 'categories']
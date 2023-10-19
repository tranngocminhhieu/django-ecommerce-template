from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
import json
from ..models import Order, OrderItem, Wishlist
from django.db.models import Q, Sum, Avg
from .serializers import OderItemSerializer

from products.api.serializers import ProductVariantSerializer, ProductSerializer
from products.models import ProductVariant, Product

@api_view(['POST'])
def edit_cart(request):
    payload = request.data
    action = payload.get('action')
    product_variant_id = payload.get('product_variant_id')
    order, created = Order.objects.get_or_create(user=request.user, status=-1)
    order_item, created = OrderItem.objects.get_or_create(order=order, product_variant_id=product_variant_id)

    if action == 'add':
        order_item.quantity = order_item.quantity + 1 if order_item.quantity else 1
        order_item.price = order_item.product_variant.price
        order_item.save()
    elif action == 'delete':
        order_item.delete()

    # order_item.product_variant.product.slug

    order_items = OrderItem.objects.filter(order=order).all()

    data = {
        'total_items': order_items.aggregate(Sum('quantity')).get('quantity__sum'),
        'total_amount': order.total_amount(),
        'items': OderItemSerializer(order_items, many=True).data,
    }


    for item in data['items']:
        product = ProductSerializer(ProductVariant.objects.get(pk=item['product_variant_id']).product).data

        item['product'] = {
            'name': product['name'],
            'slug': product['slug'],
            'image': product['image']
        }

        product_variant = ProductVariant.objects.get(pk=item['product_variant_id'])

        item['product_variant'] = {
            'version': product_variant.version.name,
            'color': {
                'color_name': product_variant.color.name,
                'color_code': product_variant.color.color_code,
                'color_image': product_variant.color.color_image or None,
            }
        }

    return Response(data=data, status=status.HTTP_201_CREATED)
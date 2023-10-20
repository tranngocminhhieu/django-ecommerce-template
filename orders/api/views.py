from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
import json
from ..models import Order, OrderItem, Wishlist
from django.db.models import Q, Sum, Avg
from .serializers import OderItemSerializer, OrderSerializer

from products.api.serializers import ProductVariantSerializer, ProductSerializer
from products.models import ProductVariant, Product


def get_cart_info(order):
    order_items = OrderItem.objects.filter(order=order).all()

    data = {
        'total_items': order_items.aggregate(Sum('quantity')).get('quantity__sum') or 0,
        'total_amount': order.total_amount(),
        'items': OderItemSerializer(order_items, many=True).data,
    }


    for item in data['items']:
        product_variant = ProductVariant.objects.get(pk=item['product_variant_id'])

        item['product_variant'] = {
            'version': product_variant.version.name,
            'color': {
                'color_name': product_variant.color.name,
                'color_code': product_variant.color.color_code,
                'color_image': product_variant.color.color_image or None,
            }
        }

        product = product_variant.product

        item['product'] = {
            'name': product.name,
            'slug': product.slug,
            'image': product.image.url
        }

    return data

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

    data = get_cart_info(order)


    return Response(data=data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def update_cart(request):
    payload = request.data # [{"product_variant_id": 1, "quantity": 3}, {"product_variant_id": 2, "quantity": 5}]

    order, created = Order.objects.get_or_create(user=request.user, status=-1)

    order_items = OrderItem.objects.filter(order=order)

    for order_item in order_items:
        if order_item.product_variant.id in [item['product_variant_id'] for item in payload]:
            order_item.quantity = [item['quantity'] for item in payload if item['product_variant_id']==order_item.product_variant.id][0]
            order_item.save()
        else:
            order_item.delete()

    data = get_cart_info(order)

    return Response(data=data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def update_draft_order(request):
    order, created = Order.objects.get_or_create(user=request.user, status=-1)
    payload = request.data

    data = OrderSerializer(order).data

    for field in payload:
        data[field] = payload[field]

    order_serializer = OrderSerializer(data=data)
    if order_serializer.is_valid():
        order_serializer.update(instance=order, validated_data=order_serializer.validated_data)

    return Response(data=order_serializer.data, status=status.HTTP_201_CREATED)
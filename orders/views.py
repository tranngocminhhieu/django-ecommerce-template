import json

from django.shortcuts import render
from .models import Order, OrderItem, ShippingMethod
# Create your views here.

def cart(request):

    order, created = Order.objects.get_or_create(user=request.user, status=-1)
    order_items = OrderItem.objects.filter(order=order)

    context = {
        'order': order,
        'order_items': order_items
    }
    return render(request=request, template_name='orders/cart.html', context=context)

def checkout_details(request):

    order, created = Order.objects.get_or_create(user=request.user, status=-1)
    order_items = OrderItem.objects.filter(order=order)

    context = {
        'order': order,
        'order_items': order_items
    }

    return render(request=request, template_name='orders/checkout/details.html', context=context)

def checkout_shipping(request):
    shipping_methods = ShippingMethod.objects.all()
    order, created = Order.objects.get_or_create(user=request.user, status=-1)
    order_items = OrderItem.objects.filter(order=order)
    context = {
        'shipping_methods': shipping_methods,
        'order': order,
        'order_items': order_items
    }
    return render(request=request, template_name='orders/checkout/shipping.html', context=context)

def checkout_payment(request):
    context = {}
    return render(request=request, template_name='orders/checkout/payment.html', context=context)

def checkout_review(request):
    context = {}
    return render(request=request, template_name='orders/checkout/review.html', context=context)
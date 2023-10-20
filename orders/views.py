import json

from django.shortcuts import render
from .models import Order, OrderItem, ShippingMethod, PromoCode
# Create your views here.

def cart(request):

    order, created = Order.objects.get_or_create(user=request.user, status=-1)
    order_items = OrderItem.objects.filter(order=order)


    if request.method == 'POST':
        code = request.POST.get('promo_code')
        try:
            promo_code = PromoCode.objects.get(code=code)
        except PromoCode.DoesNotExist:
            promo_code = None

        if promo_code:
            order.promo_code = promo_code
            order.save()

    context = {
        'order': order,
        'order_items': order_items,
        'discounted_subtotal_amount': round(order.subtotal_amount() * (1- order.promo_code.discount)) if order.promo_code else 0
    }

    return render(request=request, template_name='orders/cart.html', context=context)

def checkout_details(request):

    order, created = Order.objects.get_or_create(user=request.user, status=-1)
    order_items = OrderItem.objects.filter(order=order)

    if request.method == 'POST':
        code = request.POST.get('promo_code')
        try:
            promo_code = PromoCode.objects.get(code=code)
        except PromoCode.DoesNotExist:
            promo_code = None

        if promo_code:
            order.promo_code = promo_code
            order.save()

    context = {
        'order': order,
        'order_items': order_items
    }

    return render(request=request, template_name='orders/checkout/details.html', context=context)

def checkout_shipping(request):
    shipping_methods = ShippingMethod.objects.all()
    order, created = Order.objects.get_or_create(user=request.user, status=-1)
    order_items = OrderItem.objects.filter(order=order)

    if request.method == 'POST':
        code = request.POST.get('promo_code')
        try:
            promo_code = PromoCode.objects.get(code=code)
        except PromoCode.DoesNotExist:
            promo_code = None

        if promo_code:
            order.promo_code = promo_code
            order.save()

    context = {
        'shipping_methods': shipping_methods,
        'order': order,
        'order_items': order_items
    }
    return render(request=request, template_name='orders/checkout/shipping.html', context=context)

def checkout_payment(request):
    order, created = Order.objects.get_or_create(user=request.user, status=-1)
    order_items = OrderItem.objects.filter(order=order)

    if request.method == 'POST':
        code = request.POST.get('promo_code')
        try:
            promo_code = PromoCode.objects.get(code=code)
        except PromoCode.DoesNotExist:
            promo_code = None

        if promo_code:
            order.promo_code = promo_code
            order.save()

    context = {
        'order': order,
        'order_items': order_items
    }
    return render(request=request, template_name='orders/checkout/payment.html', context=context)

def checkout_review(request):
    order, created = Order.objects.get_or_create(user=request.user, status=-1)
    order_items = OrderItem.objects.filter(order=order)

    if request.method == 'POST':
        code = request.POST.get('promo_code')
        try:
            promo_code = PromoCode.objects.get(code=code)
        except PromoCode.DoesNotExist:
            promo_code = None

        if promo_code:
            order.promo_code = promo_code
            order.save()

    context = {
        'order': order,
        'order_items': order_items
    }
    return render(request=request, template_name='orders/checkout/review.html', context=context)

def checkout_complete(request, order_id):
    order = Order.objects.get(pk=order_id)

    if order.status == -1:
        order.status = 0
        order.save()

        for order_item in order.orderitem_set.all():
            order_item.price = order_item.product_variant.price
            order_item.save()

    order_items = OrderItem.objects.filter(order=order)

    context = {
        'order': order,
        'order_items': order_items
    }

    return render(request=request, template_name='orders/checkout/complete.html', context=context)

def order_tracking(request, order_id):
    order = Order.objects.get(pk=order_id)
    order_items = OrderItem.objects.filter(order=order)

    context = {
        'order': order,
        'order_items': order_items
    }

    return render(request=request, template_name='orders/tracking.html', context=context)



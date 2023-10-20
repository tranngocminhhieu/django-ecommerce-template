from django.db import models
from products.models import Product, ProductVariant
from django.contrib.auth.models import User
from django.db.models import Sum

class ShippingMethod(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=2550, blank=True, null=True)
    delivery_time = models.CharField(max_length=255)
    fee = models.IntegerField()

    def __str__(self):
        return self.name

# Create your models here.
class Order(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.PROTECT)
    full_name = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    shipping_method = models.ForeignKey(to=ShippingMethod, on_delete=models.PROTECT, null=True, blank=True)
    payment_method = models.CharField(max_length=255, choices=[('COD', 'COD'), ('Card', 'Card'), ('Paypal', 'Paypal')], null=True, blank=True)
    status = models.IntegerField(choices=[(-1, 'Draft'), (0, 'Created'), (1, 'Completed')])
    comment = models.TextField(max_length=2550, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'#{self.pk} {self.user.username}'

    def total_amount(self):
        total_amount = 0
        order_items = self.orderitem_set.all() # OrderItem.objects.filter(order=self)
        for order_item in order_items:
            total_amount += order_item.price * order_item.quantity

        return total_amount

    def total_items(self):
        return self.orderitem_set.all().aggregate(Sum('quantity')).get('quantity__sum') or 0


class OrderItem(models.Model):
    order = models.ForeignKey(to=Order, on_delete=models.CASCADE)
    product_variant = models.ForeignKey(to=ProductVariant, on_delete=models.PROTECT)
    price = models.IntegerField(null=True)
    quantity = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Order {self.order.pk} {self.product_variant.product.name} {self.product_variant.version} {self.product_variant.color}'

    def amount(self):
        return self.price * self.quantity

class Wishlist(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.PROTECT)
    product_variant = models.ForeignKey(to=ProductVariant, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} {self.product_variant.product.name} {self.product_variant.version.name} {self.product_variant.color.name}'
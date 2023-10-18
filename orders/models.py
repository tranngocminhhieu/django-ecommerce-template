from django.db import models
from products.models import Product, ProductVariant
from django.contrib.auth.models import User

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
    full_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, null=True, blank=True)
    shipping_method = models.ForeignKey(to=ShippingMethod, on_delete=models.PROTECT)
    payment_method = models.CharField(max_length=255, choices=[('COD', 'COD'), ('Card', 'Card'), ('Paypal', 'Paypal')])
    status = models.IntegerField(choices=[(-1, 'Draft'), (0, 'Created'), (1, 'Completed')])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'#{self.pk} {self.full_name} {self.created_at}'

class OrderItem(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    order = models.ForeignKey(to=Order, on_delete=models.CASCADE)
    product_variant = models.ForeignKey(to=ProductVariant, on_delete=models.PROTECT)
    price = models.IntegerField()
    quantity = models.IntegerField()

    def __str__(self):
        return f'Order {self.order.pk} {self.product.name}'

class Wishlist(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.PROTECT)
    product_variant = models.ForeignKey(to=ProductVariant, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} {self.product_variant.product.name} {self.product_variant.version.name} {self.product_variant.color.name}'
from django.db import models
from products.models import Product, ProductColor, Price, Version

class ShippingMethod(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=2550, blank=True, null=True)
    delivery_time = models.CharField(max_length=255)
    fee = models.IntegerField(max_length=255)

    def __str__(self):
        return self.name

# Create your models here.
class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    full_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, null=True, blank=True)
    shipping_method = models.ForeignKey(to=ShippingMethod, on_delete=models.PROTECT)
    payment_method = models.CharField(max_length=255, choices=[('COD', 'COD'), ('Card', 'Card'), ('Paypal', 'Paypal')])
    status = models.IntegerField(choices=[(-1, 'Draft'), (0, 'Created'), (1, 'Completed')])

    def __str__(self):
        return f'#{self.pk} {self.full_name} {self.created_at}'

class OrderItem(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    order = models.ForeignKey(to=Order, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.PROTECT)
    version = models.ForeignKey(to=Version, on_delete=models.PROTECT)
    product_color = models.ForeignKey(to=ProductColor, on_delete=models.PROTECT)
    price = models.IntegerField()
    quantity = models.IntegerField()

    def __str__(self):
        return f'Order {self.order.pk} {self.product.name}'


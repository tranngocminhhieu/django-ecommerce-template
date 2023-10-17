from django.contrib import admin
from .models import Order, OrderItem, ShippingMethod

# Register your models here.
def register_admin_site(model, enable_filter=False, enable_search=False):
    class ModelAdmin(admin.ModelAdmin):
        list_display = [f.name for f in model._meta.fields]
        list_filter = [f.name for f in model._meta.fields] if enable_filter else []
        search_fields = [f.name for f in model._meta.fields] if enable_search else []
    admin.site.register(model, ModelAdmin)

register_admin_site(Order)
register_admin_site(OrderItem)
register_admin_site(ShippingMethod)
from django.contrib import admin
from .models import Order, OrderItem, ShippingMethod, Wishlist

# Register your models here.
def register_admin_site(model, fileds=None, enable_filter=False, enable_search=False, hide_fileds=[]):
    list_fields = [f.name for f in model._meta.fields if f.name not in hide_fileds] if not fileds else fileds
    class ModelAdmin(admin.ModelAdmin):
        list_display = list_fields
        list_filter = list_fields if enable_filter else []
        search_fields = list_fields if enable_search else []

    admin.site.register(model, ModelAdmin)

register_admin_site(Order)
register_admin_site(OrderItem)
register_admin_site(ShippingMethod)
register_admin_site(Wishlist)
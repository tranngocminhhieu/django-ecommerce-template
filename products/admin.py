from django.contrib import admin
from .models import *

def register_admin_site(model, enable_filter=False, enable_search=False):
    class ModelAdmin(admin.ModelAdmin):
        list_display = [f.name for f in model._meta.fields]
        list_filter = [f.name for f in model._meta.fields] if enable_filter else []
        search_fields = [f.name for f in model._meta.fields] if enable_search else []
    admin.site.register(model, ModelAdmin)

register_admin_site(Category, enable_search=True)
register_admin_site(Brand, enable_search=True)
register_admin_site(Product, enable_filter=True, enable_search=True)
register_admin_site(Color, enable_search=True)
register_admin_site(Version, enable_search=True)
register_admin_site(Price, enable_filter=True, enable_search=True)
register_admin_site(Gallery, enable_search=True)
register_admin_site(Review, enable_filter=True, enable_search=True)
register_admin_site(ProductColor)
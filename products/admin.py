from django.contrib import admin
from .models import *

def register_admin_site(model, fileds=None, enable_filter=False, enable_search=False, hide_fileds=[]):
    list_fields = [f.name for f in model._meta.fields if f.name not in hide_fileds] if not fileds else fileds
    class ModelAdmin(admin.ModelAdmin):
        list_display = list_fields
        list_filter = list_fields if enable_filter else []
        search_fields = list_fields if enable_search else []

    admin.site.register(model, ModelAdmin)

register_admin_site(Category, hide_fileds=['id', 'created_at', 'updated_at'])
register_admin_site(Brand, hide_fileds=['id', 'created_at', 'updated_at'])
register_admin_site(Color, hide_fileds=['id', 'created_at', 'updated_at'])
register_admin_site(Version, hide_fileds=['id', 'created_at', 'updated_at', 'tech_specs'])
register_admin_site(ProductVariant, hide_fileds=['id', 'created_at', 'updated_at'])
register_admin_site(Gallery, hide_fileds=['id', 'created_at', 'updated_at'])
register_admin_site(Review, hide_fileds=['id', 'created_at', 'updated_at'])

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'image', 'brand', 'get_categories']
    list_display_links = ['name']
    def get_categories(self, obj):
        return [category for category in obj.categories.all()]
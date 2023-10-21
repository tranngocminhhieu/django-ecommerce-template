from .models import Category, Brand
from django.db.models import Q
def product_context(request):
    context = {
        'product_categories': Category.objects.filter(~Q(slug__in=['hot', 'trending', 'top'])),
        'product_brands': Brand.objects.all()
    }
    return context
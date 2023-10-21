from django.shortcuts import render
from products.models import Product

# Create your views here.
def home(request):
    trending_products = Product.objects.filter(categories__slug='trending')
    products = Product.objects.all()

    context = {
        'trending_products': trending_products,
        'products': products
    }
    return render(request=request, template_name='home/home.html', context=context)
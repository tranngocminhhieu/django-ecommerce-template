from django.shortcuts import render
from .models import Product, Gallery, Review,Version, ProductColor
from django.db.models import Q
from django.db.models import Avg

# Create your views here.
def product(request, slug):
    product = Product.objects.get(slug=slug)
    gallery = Gallery.objects.filter(product=product)
    reviews = Review.objects.filter(product=product)
    versions = Version.objects.filter(product=product)
    product_colors = ProductColor.objects.filter(product=product)
    related_products = Product.objects.filter(Q(categories__in=product.categories.all()) | Q(brand=product.brand)).exclude(slug=product.slug)
    context = {
        'product': product,
        'gallery': gallery,
        'related_products': related_products,
        'reviews': reviews,
        'versions': versions,
        'product_colors': product_colors
    }
    return render(request=request, template_name='products/product/index.html', context=context)
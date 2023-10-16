from django.shortcuts import render
from .models import Product, Gallery, Review,Version, ProductColor, Price
from django.db.models import Q
from django.db.models import Avg, F, Case, When, Value, IntegerField

# Create your views here.
def product(request, slug):
    product = Product.objects.get(slug=slug)
    gallery = Gallery.objects.filter(product=product)
    reviews = Review.objects.filter(product=product)
    main_price = Price.objects.filter(product=product).order_by('price').first()
    versions = Version.objects.filter(Q(product=product) & ~Q(name=main_price.version.name)).order_by('price__price')
    product_colors = ProductColor.objects.filter(product=product)

    star1 = reviews.filter(rating=1).count()
    star2 = reviews.filter(rating=2).count()
    star3 = reviews.filter(rating=3).count()
    star4 = reviews.filter(rating=4).count()
    star5 = reviews.filter(rating=5).count()
    total_reviews = reviews.count()

    review_stars_detail = {
        1: {'count': star1, 'percent': round((star1 / total_reviews)*100)},
        2: {'count': star2, 'percent': round((star2 / total_reviews)*100)},
        3: {'count': star3, 'percent': round((star3 / total_reviews)*100)},
        4: {'count': star4, 'percent': round((star4 / total_reviews)*100)},
        5: {'count': star5, 'percent': round((star5 / total_reviews)*100)},
    }

    recommended_percent = round(((star3 + star4 + star5) / total_reviews)*100)

    related_products = Product.objects.filter(Q(categories__in=product.categories.all()) | Q(brand=product.brand)).exclude(slug=product.slug)
    context = {
        'product': product,
        'gallery': gallery,
        'related_products': related_products,
        'reviews': reviews,
        'versions': versions,
        'product_colors': product_colors,
        'main_price': main_price,
        'review_stars_detail': review_stars_detail,
        'recommended_percent': recommended_percent
    }
    return render(request=request, template_name='products/product/index.html', context=context)
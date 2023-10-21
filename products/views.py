from django.shortcuts import render, get_object_or_404
from .models import Product, Gallery, Review, ProductVariant, Brand
from django.db.models import Q
from django.db.models import Avg, F, Case, When, Value, IntegerField, Max
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from orders.models import ShippingMethod

PER_PAGE = 9



# Create your views here.
def product(request, slug):
    # Use get_object_or_404 to handle the case when the product with the given slug doesn't exist.
    product = get_object_or_404(Product, slug=slug)

    # Get the default variant of the product
    default_variant = product.default_variant()

    # Get the selected color from the query parameters or use the default color
    color = request.GET.get('color', default_variant.color.name)

    # Check if the selected color is valid for the product, and if not, use the default color
    if color not in [variant.color.name for variant in ProductVariant.objects.filter(product=product)]:
        color = default_variant.color.name

    # Get the selected version from the query parameters or use the default version
    version = request.GET.get('version', default_variant.version.name)

    # Check if the selected version is valid for the product, and if not, use the default version
    if version not in [variant.version.name for variant in ProductVariant.objects.filter(product=product)]:
        version = default_variant.version.name

    # Get the main_variant based on the selected color and version
    main_variant = ProductVariant.objects.filter(Q(color__name=color) & Q(version__name=version)).first()

    product_variants = ProductVariant.objects.filter(product=product).order_by('price', '-quantity')
    gallery = Gallery.objects.filter(product=product)


    reviews = Review.objects.filter(product_variant__product=product)
    star1 = reviews.filter(rating=1).count()
    star2 = reviews.filter(rating=2).count()
    star3 = reviews.filter(rating=3).count()
    star4 = reviews.filter(rating=4).count()
    star5 = reviews.filter(rating=5).count()
    total_reviews = reviews.count()

    review_stars_detail = {
        1: {'count': star1, 'percent': round((star1 / total_reviews)*100)} if total_reviews != 0 else 0,
        2: {'count': star2, 'percent': round((star2 / total_reviews)*100)} if total_reviews != 0 else 0,
        3: {'count': star3, 'percent': round((star3 / total_reviews)*100)} if total_reviews != 0 else 0,
        4: {'count': star4, 'percent': round((star4 / total_reviews)*100)} if total_reviews != 0 else 0,
        5: {'count': star5, 'percent': round((star5 / total_reviews)*100)} if total_reviews != 0 else 0,
    }

    recommended_percent = round(((star3 + star4 + star5) / total_reviews)*100) if total_reviews != 0 else 0

    related_products = Product.objects.filter(Q(categories__in=product.categories.all()) | Q(brand=product.brand)).exclude(slug=product.slug).distinct()

    context = {
        'product': product,
        'main_variant': main_variant,
        'gallery': gallery,
        'related_products': related_products,
        'reviews': reviews,
        'product_variants': product_variants,
        'review_stars_detail': review_stars_detail,
        'recommended_percent': recommended_percent,
        'shipping_methods': ShippingMethod.objects.all()
    }
    return render(request=request, template_name='products/product/index.html', context=context)

def products(request):
    # Get all params
    page_number = request.GET.get('page', 1)
    min_price = request.GET.get('min_price', 0)
    max_price = request.GET.get('max_price', 999999999)
    brands = request.GET.getlist('brand')
    category = request.GET.get('category')

    filters = Q(productvariant__price__range=[min_price, max_price])

    if brands:
        filters &= Q(brand__name__in=brands)
    if category:
        filters &= Q(categories__name=category)

    products = Product.objects.filter(filters).distinct()

    products_paginator = Paginator(products, per_page=PER_PAGE)

    try:
        products_paginator = products_paginator.page(number=page_number)
    except PageNotAnInteger:
        products_paginator = products_paginator.page(number=1)
    except EmptyPage:
        products_paginator = products_paginator.page(number=products_paginator.num_pages)

    filter_max_price = ProductVariant.objects.aggregate(Max('price')).get('price__max')

    context = {
        'products': products_paginator,
        'filter_max_price': filter_max_price,
        'min_price': min_price,
        'max_price': max_price,
        'brands': brands,
        'category': category
    }
    view = request.GET.get('view')
    if view == 'list':
        return render(request=request, template_name='products/products_list.html', context=context)
    else:
        return render(request=request, template_name='products/products_grid.html', context=context)
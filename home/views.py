from django.shortcuts import render
from products import models as products_models

# Create your views here.
def home(request):
    brands = products_models.Brand.objects.all()
    # user
    context = {
        'brands': brands
    }
    return render(request=request, template_name='home/home.html', context=context)
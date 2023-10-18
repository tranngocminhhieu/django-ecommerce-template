import json

from django.shortcuts import render
from .models import Order, OrderItem
# Create your views here.

def edit_cart(request):
    data = json.loads(request.body)
    action = data.get('action')

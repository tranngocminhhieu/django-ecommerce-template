from django.urls import path, include
from . import views

app_name = 'orders'

urlpatterns = [
    path('api/', include('orders.api.urls')),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout_details, name='checkout_details'),
    path('checkout/shipping/', views.checkout_shipping, name='checkout_shipping'),
    path('checkout/payment/', views.checkout_payment, name='checkout_payment'),
    path('checkout/review/', views.checkout_review, name='checkout_review'),
]
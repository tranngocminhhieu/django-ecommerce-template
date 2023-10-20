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
    path('checkout/complete/<int:order_id>', views.checkout_complete, name='checkout_complete'),
    path('order-tracking/<int:order_id>', views.order_tracking, name='order_tracking'),
]
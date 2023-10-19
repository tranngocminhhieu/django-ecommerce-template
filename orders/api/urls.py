from django.urls import path
from . import views

urlpatterns = [
    path('edit-cart/', views.edit_cart, name='api_edit_cart')
]
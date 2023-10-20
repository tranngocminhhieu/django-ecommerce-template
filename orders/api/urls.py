from django.urls import path
from . import views

urlpatterns = [
    path('edit-cart/', views.edit_cart, name='api_edit_cart'),
    path('update-cart/', views.update_cart, name='api_update_cart'),
    path('update-draft-order/', views.update_draft_order, name='api_update_draft_order'),
    path('edit-wishlist/', views.edit_wishlist, name='api_edit_wishlist'),
]
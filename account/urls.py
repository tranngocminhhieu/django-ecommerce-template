from django.urls import path, include
from . import views

app_name = 'account'

urlpatterns = [
    path('api/', include('account.api.urls')),
    path('signin/', views.signin, name='signin'),
    path('orders/', views.orders, name='orders'),
    path('signout/', views.signout, name='signout'),
]
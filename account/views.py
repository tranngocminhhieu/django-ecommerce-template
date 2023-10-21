from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from orders.models import Order, Wishlist
from django.db.models import Q
from django.contrib.auth.decorators import login_required


# Create your views here.
def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        is_auth = authenticate(username=username, password=password)

        if is_auth:
            login(request=request, user=is_auth)
            return redirect(to='home:home')

    if request.user.is_authenticated:
        return redirect(to='home:home')

    return render(request=request, template_name='account/signin.html')

def signout(request):
    logout(request)
    return redirect(to='account:signin')

@login_required
def orders(request):
    if not request.user.is_authenticated:
        return redirect(to='account:signin')

    orders = Order.objects.filter(~Q(status=-1) & Q(user=request.user))
    wishlist = Wishlist.objects.filter(user=request.user)

    context = {
        'orders': orders,
        'wishlist': wishlist,
    }

    return render(request=request, template_name='account/orders.html', context=context)

@login_required
def profile(request):
    if not request.user.is_authenticated:
        return redirect(to='account:signin')

    orders = Order.objects.filter(~Q(status=-1) & Q(user=request.user))
    wishlist = Wishlist.objects.filter(user=request.user)

    context = {
        'orders': orders,
        'wishlist': wishlist,
    }
    return render(request=request, template_name='account/profile.html', context=context)

@login_required
def wishlist(request):
    if not request.user.is_authenticated:
        return redirect(to='account:signin')

    orders = Order.objects.filter(~Q(status=-1) & Q(user=request.user))
    wishlist = Wishlist.objects.filter(user=request.user)

    context = {
        'orders': orders,
        'wishlist': wishlist,
    }
    return render(request=request, template_name='account/wishlist.html', context=context)

@login_required
def address(request):
    if not request.user.is_authenticated:
        return redirect(to='account:signin')

    orders = Order.objects.filter(~Q(status=-1) & Q(user=request.user))
    wishlist = Wishlist.objects.filter(user=request.user)

    context = {
        'orders': orders,
        'wishlist': wishlist,
    }
    return render(request=request, template_name='account/address.html', context=context)
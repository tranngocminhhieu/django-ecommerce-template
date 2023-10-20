from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

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

def orders(request):
    if not request.user.is_authenticated:
        return redirect(to='account:signin')
    else:
        user = User.objects.get(username=request.user.username)
        context = {
            'user': user
        }
        return render(request=request, template_name='account/orders.html', context=context)

def profile(request):
    if not request.user.is_authenticated:
        return redirect(to='account:signin')
    else:
        user = User.objects.get(username=request.user.username)
        context = {
            'user': user
        }
        return render(request=request, template_name='account/profile.html', context=context)

def wishlist(request):
    context = {}
    return render(request=request, template_name='account/wishlist.html', context=context)